#!/usr/bin/env python
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Everyone sends a single object to every MPI processes
results = comm.allgather(rank)

print 'rank: %d; results: %r' % (rank, results)

# This is equivalent
results = comm.gather(rank, root=0)
results = comm.bcast(results, root=0)

print 'rank: %d; results: %r' % (rank, results)
