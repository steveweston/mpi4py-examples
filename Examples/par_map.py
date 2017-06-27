#!/usr/bin/env python
from math import sqrt
from mpi4py import MPI

def myslice(n, size, rank):
    m, r = divmod(n, size)
    if r > 0:
        m += 1
    start = rank * m
    end = min(start + m, n)
    return slice(start, end)

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

x = range(20)

# Get chunk of "x" for this rank and perform computation on it
x_chunk = x[myslice(len(x), size, rank)]
r_chunk = map(sqrt, x_chunk)

# Combine all the result chunks
r_chunks = comm.gather(r_chunk)
if rank == 0:
    r = [y for x in r_chunks for y in x]
    print "gather:", r

# Alternative method to combine all the result chunks
r = comm.reduce(r_chunk)
if rank == 0:
    print "reduce:", r

# All processes get the combined result chunks
r = comm.allreduce(r_chunk)
print "reduce:", r
