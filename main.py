from mpi4py import MPI
from web3 import Web3, HTTPProvider
import time
import psutil
import os

comm = MPI.COMM_WORLD # commutator
rank = comm.rank # rank of process
size = comm.size # size of all processes

cpu_to_eth_rate = 0.01 # 0.01 ETH/second of cpu time
mem_to_eth_rate = 0.005 # 0.005 ETH/MB of memory space

web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/6e7e72b8ca844879b9ecc344bd8965df")) # connect to Infura host node in order to connect with Ethereum network (Ropsten)

# returns memory usage for process in MB
def memory_usage_psutil():
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20) # fixed at four decimal places
    return mem

def compute_fun(x):
    fun = pow(x, 3) - 4 * (pow(x, 2)) + 7 # defined function (MAKE USER DEFINED)
    return fun

def compute_integral(N,lower_lim,upper_lim):
   i = 0
   area = 0.0
   increment_val = (upper_lim - lower_lim)/(N-1)
   for i in range(0, N):
       area = area + (increment_val)*compute_fun(lower_lim+(i*increment_val)) # derived from Reimann's sum formula
   return area

def send_ether_to_wallet(wallet_address_from, wallet_address_to, wallet_private_key, amount_in_ether):
    amount_in_wei = web3.toWei(amount_in_ether,'ether')

    nonce = web3.eth.getTransactionCount(wallet_address_from)

    txn_dict = {
            'to': wallet_address_to,
            'value': amount_in_wei,
            'gas': 2000000,
            'gasPrice': web3.toWei('40', 'gwei'),
            'nonce': nonce,
            'chainId': 3
    }

    signed_txn = web3.eth.account.signTransaction(txn_dict, wallet_private_key)

    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    txn_receipt = None

    count = 0

    while txn_receipt is None and (count < 30):
        txn_receipt = web3.eth.getTransactionReceipt(txn_hash)
        time.sleep(10)

    if txn_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}

    return {'status': 'added', 'txn_receipt': txn_receipt}

def main ():
    if rank == 0: # world computer
        wallet_private_key = "cfcb8acfd0b4c64a6b6366f79c97aa7502396ffd6c61dc92c8e8befcafa72311"
        wallet_address_from = web3.toChecksumAddress("0x93501acf5ec5f2ee2c1372142762d9bb75e8b607")

        # define limits of integral and number of points used in Reimann's sum
        lower_lim = -1.0
        upper_lim = 1.0
        N = 10

        # send variable information to slave computer #1
        comm.send(lower_lim, dest=1, tag=0)
        comm.send(upper_lim, dest=1, tag=1)
        comm.send(N, dest=1, tag=2)

        # send variable information to slave computer #2
        comm.send(lower_lim, dest=2, tag=0)
        comm.send(upper_lim, dest=2, tag=1)
        comm.send(N, dest=2, tag=2)

        fee = comm.recv(source=1, tag=3)
        wallet_address_to = comm.recv(source=1, tag=4)
        send_ether_to_wallet(wallet_address_from, wallet_address_to, wallet_private_key, fee)

        fee = comm.recv(source=2, tag=3)
        wallet_address_to = comm.recv(source=2, tag=4)
        send_ether_to_wallet(wallet_address_from, wallet_address_to, wallet_private_key, fee)
    elif rank == 1: # slave computer #1
        wallet_address_to = web3.toChecksumAddress("0x4DAb2824A4dF9ac5366Cd381839192A2223E3bEd")

        lower_lim = comm.recv(source=0, tag=0)
        upper_lim = comm.recv(source=0, tag=1)
        N = comm.recv(source=0, tag=2)

        lower_lim_new = lower_lim
        upper_lim_new = ((upper_lim - lower_lim) / 2) + lower_lim # split limits of integral in half (PARALLELIZATION)
        area = compute_integral(N, lower_lim_new, upper_lim_new) # compute area of own half

        cpu_time = time.process_time()  # following statement assumed to be negligible
        mem_usg = memory_usage_psutil()  # end of process (print statement not to be included)

        fee = cpu_time * cpu_to_eth_rate + mem_usg * mem_to_eth_rate
        comm.send(fee, dest=0, tag=3)

        comm.send(wallet_address_to, dest=0, tag=4)

        print("Rank " + str(rank) + " out of " + str(size) + " processors. Area: " + str(area) + "; CPU time: "
              + str(cpu_time) + " s " + "; Memory usage: " + str(mem_usg) + " MB")
    elif rank == 2: # slave computer #2
        wallet_address_to = web3.toChecksumAddress("0x14CB89A6154048EAe1991d4A1e13a6B8Cc59F97B")

        lower_lim = comm.recv(source=0, tag=0)
        upper_lim = comm.recv(source=0, tag=1)
        N = comm.recv(source=0, tag=2)

        lower_lim_new = lower_lim
        upper_lim_new = ((upper_lim - lower_lim) / 2) + lower_lim # split limits of integral in half (PARALLELIZATION)
        area = compute_integral(N, lower_lim_new, upper_lim_new) # compute area of own half

        cpu_time = time.process_time() # following statement assumed to be negligible
        mem_usg = memory_usage_psutil() # end of process (print statement not to be included)

        fee = cpu_time * cpu_to_eth_rate + mem_usg * mem_to_eth_rate
        comm.send(fee, dest=0, tag=3)

        comm.send(wallet_address_to, dest=0, tag=4)

        print("Rank " + str(rank) + " out of " + str(size) + " processors. Area: " + str(area) + "; CPU time: "
              + str(cpu_time) + " s " + "; Memory usage: " + str(mem_usg) + " MB")

main()