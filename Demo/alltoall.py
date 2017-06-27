#!/usr/bin/env python
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# 
results = comm.alltoall([i + 10 * rank for i in range(size)])

print 'rank: %d; results: %r' % (rank, results)
