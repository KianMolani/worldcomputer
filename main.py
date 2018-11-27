from mpi4py import MPI
from web3 import Web3, HTTPProvider
import time
import psutil
import os

comm = MPI.COMM_WORLD # commutator
rank = comm.rank # rank of process
size = comm.size # size of all processes

cpu_to_eth_rate = 0.01 # 0.01 ETH/second of cpu time (arbitrary)
mem_to_eth_rate = 0.005 # 0.005 ETH/MB of memory space (arbitrary)

web3 = Web3(HTTPProvider("ENTER INFURA KEY FOR ROPSTEN NETWORK HERE")) # connect to Ethereum (Ropsten) network through Infura host node

# returns memory usage for process in MB
def memory_usage_psutil():
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20) # fixed at four decimal places
    return mem

# compute value of a user-defined function
def compute_fun(x):
    fun = pow(x, 3) - 4 * (pow(x, 2)) + 7 # f(x) = x^3 - 4*x^2 + 7
    return fun

# compute the value of an integral given a function, limits, and a number of points
def compute_integral(N,lower_lim,upper_lim):
   i = 0
   area = 0.0
   rect_width = (upper_lim - lower_lim)/(N-1) # width of a "rectangle"
   for i in range(0, N):
       area = area + (rect_width) * compute_fun(lower_lim + (i * increment_val)) # derived from Reimann's sum   
   return area

# payment to wallets, from world computer to worker nodes
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
        txn_receipt = web3.eth.getTransactionReceipt(txn_hash) # transaction receipt returned after having been successfully mined
        time.sleep(10)

    if txn_receipt is None:
        return {'status': 'failed', 'error': 'timeout'} # transaction hasn't been mined after 5 minutes

    return {'status': 'added', 'txn_receipt': txn_receipt} # transaction has been successfully mined within 5 minutes time

def main ():
    if rank == 0: # rank 0 given to world computer (i.e. device requesting use of computational resources)
        wallet_private_key = "ENTER WORLD COMPUTER PRIVATE KEY HERE" # WARNING: CONSIDERING THAT THE SAME MPI PROGRAM IS SHARED BETWEEN NODES, WALLET PRIVATE KEY SHOULD NOT BE CONTAINED WITHIN SOURCE CODE 
        wallet_address_from = web3.toChecksumAddress("ENTER WORLD COMPUTER WALLET ADDRESS HERE")

        # define limits of integral and number of points used in Reimann's sum
        lower_lim = -1.0
        upper_lim = 1.0
        N = 10

        # send variable information to worker node #1
        comm.send(lower_lim, dest=1, tag=0)
        comm.send(upper_lim, dest=1, tag=1)
        comm.send(N, dest=1, tag=2)

        # send variable information to worker node #2
        comm.send(lower_lim, dest=2, tag=0)
        comm.send(upper_lim, dest=2, tag=1)
        comm.send(N, dest=2, tag=2)

        fee = comm.recv(source=1, tag=3) # receive fee amount from worker node #1
        wallet_address_to = comm.recv(source=1, tag=4) # receive wallet address of worker node #1
        send_ether_to_wallet(wallet_address_from, wallet_address_to, wallet_private_key, fee) # send ether to worker node #1

        fee = comm.recv(source=2, tag=3) # receive fee amount from worker node #2
        wallet_address_to = comm.recv(source=2, tag=4) # receive wallet address of worker node #2
        send_ether_to_wallet(wallet_address_from, wallet_address_to, wallet_private_key, fee) # send ether to worker node #2
    elif rank == 1: # rank 1 given to worker node #1
        wallet_address_to = web3.toChecksumAddress("ENTER WORKER NODE #1 WALLET ADDRESS HERE")

        # receive variable information sent from world computer
        lower_lim = comm.recv(source=0, tag=0)
        upper_lim = comm.recv(source=0, tag=1)
        N = comm.recv(source=0, tag=2)
        
        lower_lim_new = lower_lim
        upper_lim_new = ((upper_lim - lower_lim) / 2) + lower_lim # split limits of integral in half for PARALLELIZATION
        area = compute_integral(N, lower_lim_new, upper_lim_new) # compute area of one half

        # execution of following statements assumed to be negligible in calculation of cpu time and memory usage
        
        cpu_time = time.process_time()
        mem_usg = memory_usage_psutil()

        fee = cpu_time * cpu_to_eth_rate + mem_usg * mem_to_eth_rate
        comm.send(fee, dest=0, tag=3) # send fee amount to world computer

        comm.send(wallet_address_to, dest=0, tag=4) # send wallet address to world computer

        print("Rank " + str(rank) + " out of " + str(size) + " processors. Area: " + str(area) + "; CPU time: "
              + str(cpu_time) + " s " + "; Memory usage: " + str(mem_usg) + " MB")
    elif rank == 2: # slave computer #2
        wallet_address_to = web3.toChecksumAddress("ENTER WORKER NODE #2 WALLET ADDRESS HERE")
        
        # receive variable information sent from world computer
        lower_lim = comm.recv(source=0, tag=0)
        upper_lim = comm.recv(source=0, tag=1)
        N = comm.recv(source=0, tag=2)

        lower_lim_new = lower_lim
        upper_lim_new = ((upper_lim - lower_lim) / 2) + lower_lim # split limits of integral in half for PARALLELIZATION
        area = compute_integral(N, lower_lim_new, upper_lim_new) # compute area of one half

        # execution of following statements assumed to be negligible in calculation of cpu time and memory usage
        
        cpu_time = time.process_time()
        mem_usg = memory_usage_psutil()

        fee = cpu_time * cpu_to_eth_rate + mem_usg * mem_to_eth_rate
        comm.send(fee, dest=0, tag=3) # send fee amount to world computer

        comm.send(wallet_address_to, dest=0, tag=4) # send wallet address to world computer

        print("Rank " + str(rank) + " out of " + str(size) + " processors. Area: " + str(area) + "; CPU time: "
              + str(cpu_time) + " s " + "; Memory usage: " + str(mem_usg) + " MB")

main()
