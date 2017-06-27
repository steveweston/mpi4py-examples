#!/bin/bash
mpirun -n 4 python Send.py
mpirun -n 4 python SendMatrix.py
mpirun -n 4 python allgather.py
mpirun -n 4 python alltoall.py
mpirun -n 4 python bcast.py
mpirun -n 4 python gather.py
mpirun -n 4 python reduce.py
# mpirun -n 4 python ring1.py  # this correctly hangs
mpirun -n 4 python ring2.py
mpirun -n 4 python ring3.py
mpirun -n 4 python ring4.py
mpirun -n 4 python scatter.py
mpirun -n 4 python Probe.py
python typedict.py
