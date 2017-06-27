#!/usr/bin/env python
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
ncols = 8
x = np.zeros(ncols, dtype=np.int32)
x[:] = rank
cnt = [ncols] * size
dsp = [ncols * i for i in range(size)]

y = np.zeros((size, ncols), dtype=np.int32)
comm.Allgatherv([x, ncols, MPI.INT],
                [y, (cnt, dsp), MPI.INT])
if rank == 0:
    print(y)

y = np.zeros((size, ncols), dtype=np.int32)
y[rank,:] = x
comm.Allgatherv(MPI.IN_PLACE, [y, (cnt, dsp), MPI.INT])
if rank == 0:
    print(y)
