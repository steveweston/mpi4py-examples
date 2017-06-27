#!/usr/bin/env python
from math import sqrt
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

x = range(20)
m = len(x) // size  # make assumptions for simplicity...
x_chunk = x[rank*m:(rank+1)*m]
r_chunk = map(sqrt, x_chunk)
r = comm.allreduce(r_chunk)
print r
