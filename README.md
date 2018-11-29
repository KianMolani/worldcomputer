# World Computer Project

**Project Description**: the aim of this project is to build a device that contains no major hardware components, including, but not limited to, storage, memory, CPUs, and GPUs. Instead, all of the computationally intensive tasks are offloaded to fully rigged computers, and are only done so *on-demand*. The anticipated benefits of this model are:

* *Reduction in the cost of user-end devices*. The logic behind this stems from the fact that even when users’ computers are powered on, most of their computational resources are sitting idle most of the time. In our case, computational resources never sit idle – computation is provided and payed for on-demand.

* *A more varied, flexible, and powerful array of display technologies*. Displays are one of the most actively developed technologies on consumer markets today. However, it is sometimes difficult to integrate these advancements into users’ devices. With much of the internal hardware out of the way, however, it becomes easier for consumer devices to make use of technologies such as flexible OLEDS, smart glasses (which are usually thick and clunky), and bionic contact lenses.

* *Limitless performance*. If well managed, users should never have their performance bottle- necked by limiting hardware components. If a user needs more computational resources to carry out their tasks without performance losses, they will get it. This provides for a better and more consistent user-experience.

* *Contiguous performance across all form factors*. All user-end devices, no matter the size or form of its display, can tap into the same levels of computational resources, since none of that hardware is located internally within the devices themselves. Today, larger devices with larger displays can afford to pack in more powerful hardware components, while smaller devices with smaller displays cannot. This places limits on the use-cases that are made available across different device form factors.

* *Contiguous user-experience and interfaces across all form factors*. Since all of the computation is done and managed externally, over time users can set up hardware and software profiles across all of their devices. Again, since the computational capacity across each device does not vary, all devices can afford to run the same set of software applications. This makes user-experiences between devices more contiguous.

* *Reduced power requirements and longer battery life*. This allows for the further development of technologies where power requirements are an issue (see bionic contact lens).

* *Limitless device life-cycles*. Because it is no longer users’ responsibilities to maintain and upgrade their hardware, their devices can, in theory, be used forever. The incentive to upgrade their devices comes from the introduction of newer and more advanced displays, cameras, etc. If users happen to damage their devices, replacement costs will be cheaper (refer to first point).

* *Reduction of electronic waste*. If the entity buying and managing the actual computers/worker nodes is a corporation, they might be more incentivized to recycle their hardware components than consumers are.

**Model Diagram**:

The following repository contains two files:

    1. A document detailing preliminary research findings

    2. A python program that has a device (the "world computer") offload to two computers (the "worker nodes") the computation necessary          to calculate the area underneath a curve. Payment is made by the world computer to the worker nodes via microtransactions made            over the Ethereum network. The metrics used to calculate the payment amount are dedicated CPU time and memory space. In future            versions, additional charges will be made on the basis of bandwidth. Ultimately, this program makes practical use of several              important and relevant topics, such as: computational offloading and distributed and parallel computing. The APIs used as part of          this program are: mpi4py (Message Passing Interface for Python), web3, and Infura.
