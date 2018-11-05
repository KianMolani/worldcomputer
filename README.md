# World Computer Project

**Project Description**: the aim of this project is to build a device that contains no major hardware components, including, but not limited to, storage, memory, CPUs, and GPUs. Instead, all of the computationally intensive tasks are offloaded to fully rigged computers, and are only done so *on-demand*. 

The following repository contains two files:
    
    - a document detailing preliminary research findings
    
    - a python program (showcased at ETHSanFranciso 2018) that has a device ('world computer') offload the processing 
      required to calculate the area underneath a curve to two computers ('worker nodes') to run in parallel. Payment is
      made by the world computer to the worker nodes via microtransactions on the Ethereum network. Metrics used to 
      calculate the payment amount was dedicated CPU time and memory space, not bandwidth. This program makes practical 
      use of several important and relevant topics, such as: computational offloading and distributed and parallel 
      computing. APIs used: MPI (message passing interface), web3, and Infura.
