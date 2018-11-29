# World Computer Project

The aim of this project is to build a functioning device that contains no major hardware components, including, but not limited to, storage, memory, CPUs, and GPUs. Instead, all of the computationally intensive tasks are offloaded to fully rigged computers, and are only done so *on-demand*.

This repository contains two primary files:

1. A document detailing preliminary research findings, the purpose of which is to test the technical limitations of this technology and see if it is economically viable.

2. A python program that has a device (the "world computer") offload to two computers (the "worker nodes") the computation necessary to calculate the area underneath a curve. Payment is made by the world computer to the worker nodes via microtransactions made over the Ethereum network. The metrics used to calculate the payment amount are dedicated CPU time and memory space. In future versions, additional charges will be made on the basis of bandwidth. This program makes practical use of several important and relevant topics, mainly computational offloading and distributed and parallel computing. The APIs used as part of this program are: mpi4py (Message Passing Interface for Python), web3, and Infura.

## Prerequisites

* An implementation of MPI. For our python program, use mpich. For Mac users, mpich can be installed using the following command in terminal:

      brew install mpich

* Python3. For Mac users, python3 can be installed using the following command in terminal:

      brew install python3

* MPI for Python package. For Mac users, mpi4py can be installed using the following command in terminal:

      pip3 install mpi4py
      
* web3 API for Python. For Mac users, web3.py can be installed using the following command in terminal:

      pip install web3

## Usage

1. After downloading the repository, go into main.py and modify lines 28, 91, 92, 120, and 145 with the appropriate keys and addresses.

2. In terminal, navigate to the directory of the downloaded repository.

3. Type and run the following command in terminal:

        mpiexec -n 3 python3 main.py
