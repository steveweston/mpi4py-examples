#!/usr/bin/env python
import sys
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#
results = comm.gather(rank, root=0)

print 'rank: %d; results: %r' % (rank, results)
sys.stdout.flush()

#
comm.barrier()
print 'rank: %d; barrier' % rank
sys.stdout.flush()

#
results = comm.gather((rank, size), root=1)

print 'rank: %d; results: %r' % (rank, results)
