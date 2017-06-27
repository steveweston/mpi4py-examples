#!/usr/bin/env python
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# One process sends a different object to each of the MPI processes
results = comm.scatter(range(size), root=0)

print 'rank: %d; results: %r' % (rank, results)
