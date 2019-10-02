# World Computer Project

The aim of this project is to build a fully functioning device that contains no major internal hardware components, including but not limited to, storage, memory, CPUs, and GPUs. Instead, all of the computationally intensive tasks are offloaded to a decentralized network of computers, and are only done so *on-demand*. Requests made by this device might include, amongst other things, the rendering of images, in which case the computers doing the rendering will send bitmaps back to the device for it to display.

This project folder contains multiple files:

* A document detailing preliminary research findings, the purpose of which is to test the technical limitations of this technology and see if it is economically viable

* A python program that has a device offload to two computers (i.e. world computers) the computation necessary to calculate the area underneath a curve. Parallelization of the task is handled with the help of the Message Passing Interface (MPI). Payment is made by the device to the world computers via microtransactions made over the Ethereum network. The metrics used to calculate the payment amount are dedicated CPU time and memory space. In future versions, additional charges will be made on the  basis of bandwidth. The APIs used as part of this program are: mpi4py (Message Passing Interface for Python), web3, and Infura

* Arduino code used to integrate an LCD display and two ESP-01 ESP8266 wifi modules to the network

Development of the project is part of a broader investigation on the effectiveness of computational offloading as a use case for 5G. I have written a Medium article that describes in more detail my motivation for this endeavor: https://medium.com/@kianmolani/the-world-computer-evolving-past-the-smartphone-era-65643cbd1560

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
        
 Note: The program takes a few minutes to run to completion, since it waits for the transactions to be mined.
