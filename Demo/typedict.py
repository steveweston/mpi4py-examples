#!/usr/bin/env python
from mpi4py import MPI

print "Warning: This only works with mpi4py 2.X, not 1.X!"

chars = sorted(MPI._typedict.keys())
for k in chars:
  for m in MPI.__dict__:
    if MPI._typedict[k] is MPI.__dict__[m]:
      print "Numpy: %s\tMPI.%s" % (k, m)
