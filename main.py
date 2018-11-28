'''This program uses the Message Passing Interface (MPI) to parallelize the task of calculating the area underneath

a curve (an embarrassingly parallel task). There are three nodes/processes involved here -- a "world computer" that

defines the parameters and makes a request for computation, but uses next to no computational resources itself, and

two "worker nodes" that carry out the vast majority of the computation. These worker nodes are compensated with payment,

which is facilitated through the Ethereum network. Note that this program treats each of the host computer's CPU nodes

as individual computer/processes. In later versions, users will have the option of specifying IP addresses of computers

with distinct memory spaces'''

from mpi4py import MPI
from web3 import Web3, HTTPProvider
import time
import psutil
import os

comm = MPI.COMM_WORLD  # commutator
rank = comm.rank  # rank of process
size = comm.size  # size of all processes

cpu_to_eth_rate = 0.01  # 0.01 ETH/second of cpu time (arbitrary)
mem_to_eth_rate = 0.005  # 0.005 ETH/MB of memory space (arbitrary)

web3 = Web3(HTTPProvider("ENTER INFURA ROPSTEN ENDPOINT HERE"))  # connect to Ethereum network via Infura host node


# returns memory usage for process in MB
def memory_usage_psutil():
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)  # fixed at four decimal places
    return mem


# compute value of a user-defined function
def compute_fun(x):
    fun = pow(x, 3) - 4 * (pow(x, 2)) + 7  # f(x) = x^3 - 4x^2 + 7
    return fun


# compute the value of an integral given a function, limits, and a number of points
def compute_integral(N, lower_lim, upper_lim):
    i = 0
    area = 0.0
    rect_width = (upper_lim - lower_lim) / (N - 1)  # width of a "Reimann rectangle"
    for i in range(0, N):
        area = area + (rect_width) * compute_fun(lower_lim + (i * rect_width))  # derived from Reimann's sum
    return area


# make payment to wallet (from world computer to worker nodes, in our case)
def send_ether_to_wallet(wallet_address_from, wallet_address_to, wallet_private_key, amount_in_ether):
    amount_in_wei = web3.toWei(amount_in_ether, 'ether')

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
        txn_receipt = web3.eth.getTransactionReceipt(txn_hash)  # transaction receipt returned after having been successfully mined
        time.sleep(10)

    if txn_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}  # transaction hasn't been mined after 5 minutes

    print("Transaction from " + wallet_address_from + " to " + wallet_address_to + " for the amount of " + str(amount_in_ether) + "ETH has been successfully mined! Transaction hash: " + txn_hash.hex() + "\n")

    return {'status': 'added', 'txn_receipt': txn_receipt}  # transaction has been successfully mined within 5 minutes


def main():
    if rank == 0:  # rank 0 given to world computer (i.e. device requesting use of computational resources)
        wallet_private_key = "ENTER WORLD COMPUTER PRIVATE KEY HERE"  # WARNING: CONSIDERING THAT THE SAME MPI PROGRAM IS SHARED BETWEEN NODES, WALLET PRIVATE KEY SHOULD NOT BE CONTAINED WITHIN SOURCE CODE
        wallet_address_from = web3.toChecksumAddress("ENTER WORLD COMPUTER WALLET ADDRESS HERE")

        # define limits of integral and number of points used in Reimann's sum
        lower_lim = -1.0
        upper_lim = 1.0
        N = 10  # changes accuracy of solution

        # send variable information to worker node #1
        comm.send(lower_lim, dest=1, tag=0)
        comm.send(upper_lim, dest=1, tag=1)
        comm.send(N, dest=1, tag=2)

        # send variable information to worker node #2
        comm.send(lower_lim, dest=2, tag=0)
        comm.send(upper_lim, dest=2, tag=1)
        comm.send(N, dest=2, tag=2)

        area_total = comm.recv(source=2, tag=4)  # solution sent to us by worker node #2

        fee = comm.recv(source=1, tag=4)  # receive fee amount from worker node #1
        wallet_address_to = comm.recv(source=1, tag=5)  # receive wallet address of worker node #1
        send_ether_to_wallet(wallet_address_from, wallet_address_to, wallet_private_key, fee)  # send ether to worker node #1

        fee = comm.recv(source=2, tag=5)  # receive fee amount from worker node #2
        wallet_address_to = comm.recv(source=2, tag=6)  # receive wallet address of worker node #2
        send_ether_to_wallet(wallet_address_from, wallet_address_to, wallet_private_key, fee)  # send ether to worker node #2
    
    elif rank == 1:  # rank 1 given to worker node #1
        wallet_address_to = web3.toChecksumAddress("ENTER WORKER NODE #1 WALLET ADDRESS HERE")

        # receive variable information sent from world computer
        lower_lim = comm.recv(source=0, tag=0)
        upper_lim = comm.recv(source=0, tag=1)
        N = comm.recv(source=0, tag=2)

        lower_lim_new = lower_lim
        upper_lim_new = ((upper_lim - lower_lim) / 2) + lower_lim  # split limits of integral in half for PARALLELIZATION
        area_left_half = compute_integral(N, lower_lim_new, upper_lim_new)  # compute area of left half

        comm.send(area_left_half, dest=2, tag=3)  # send value of half-area to worker node #2

        cpu_time = time.process_time()
        mem_usg = memory_usage_psutil()

        # execution of following statements assumed to be negligible in calculation of cpu time and memory usage

        fee = cpu_time * cpu_to_eth_rate + mem_usg * mem_to_eth_rate
        comm.send(fee, dest=0, tag=4)  # send fee amount to world computer
        comm.send(wallet_address_to, dest=0, tag=5)  # send wallet address to world computer

        print("\nRank " + str(rank) + " out of " + str(size) + " processors (worker node #1) -- Area of left half: " + str(area_left_half) + "; CPU time: " + str(cpu_time) + "s; " + "Memory usage: " + str(mem_usg) + "MB")
    
    elif rank == 2:  # rank 2 given to worker node #2
        wallet_address_to = web3.toChecksumAddress("ENTER WORKER NODE #2 WALLET ADDRESS HERE")

        # receive variable information sent from world computer
        lower_lim = comm.recv(source=0, tag=0)
        upper_lim = comm.recv(source=0, tag=1)
        N = comm.recv(source=0, tag=2)

        lower_lim_new = lower_lim
        upper_lim_new = ((upper_lim - lower_lim) / 2) + lower_lim  # split limits of integral in half for PARALLELIZATION
        area_right_half = compute_integral(N, lower_lim_new, upper_lim_new)  # compute area of right half

        cpu_time = time.process_time()
        mem_usg = memory_usage_psutil()

        print("\nRank " + str(rank) + " out of " + str(size) + " processors (worker node #2) -- Area of right half: " + str(area_right_half) + "; CPU time: " + str(cpu_time) + "s; " + "Memory usage: " + str(mem_usg) + "MB")

        area_left_half = comm.recv(source=1, tag=3) # receive area of left half from worker node #1
        area_total = area_left_half + area_right_half # sum areas of right half and left half together
        comm.send(area_total, dest=0, tag=4) # send solution to world computer

        cpu_time = time.process_time()
        mem_usg = memory_usage_psutil()

        # execution of following statements assumed to be negligible in calculation of cpu time and memory usage

        fee = cpu_time * cpu_to_eth_rate + mem_usg * mem_to_eth_rate
        comm.send(fee, dest=0, tag=5)  # send fee amount to world computer
        comm.send(wallet_address_to, dest=0, tag=6)  # send wallet address to world computer

        print("\nRank " + str(rank) + " out of " + str(size) + " processors (worker node #2) -- Total area: " + str(area_total) + "; CPU time (updated): " + str(cpu_time) + "s; " + "Memory usage (updated): " + str(mem_usg) + "MB. Sending solution to world computer...\n")

main()
