#!/usr/bin/env python
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#
results = comm.reduce(rank, op=MPI.SUM, root=0)

print 'rank: %d; results: %r' % (rank, results)

# MPI.MAX
# MPI.MIN
# MPI.SUM
# MPI.PROD
# MPI.LAND
# MPI.BAND
# MPI.LOR
# MPI.BOR
# MPI.LXOR
# MPI.BXOR
# MPI.MAXLOC
# MPI.MINLOC
