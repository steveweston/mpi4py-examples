#!/usr/bin/env python
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# 
results = comm.bcast(rank, root=0)

print 'rank: %d; results: %r' % (rank, results)
