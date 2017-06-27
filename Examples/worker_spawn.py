#!/usr/bin/env python
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

initcomm = MPI.Comm.Get_parent()
test = np.empty(3, dtype=np.int64)

# mpi4py 1.x
#mpitype = MPI.__TypeDict__[test.dtype.char]
# mpi4py 2.x
mpitype = MPI._typedict[test.dtype.char]

print("Bcast coming to rank {0}".format(rank))
initcomm.Bcast([test, mpitype], root=0)
print("Received {0}".format(test))
initcomm.Disconnect()
