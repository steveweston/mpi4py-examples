#!/usr/bin/env python
import sys,time
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

initcomm = MPI.COMM_SELF.Spawn(sys.executable, args=['worker_spawn.py'],
                               maxprocs=5)
test = np.array([1,2,3], dtype=np.int64)

# mpi4py 1.x
#mpitype = MPI.__TypeDict__[test.dtype.char]
# mpi4py 2.x
mpitype = MPI._typedict[test.dtype.char]

print("About to broadcast {0} from rank {1}".format(test, rank))
initcomm.Bcast([test, mpitype], root=MPI.ROOT)
initcomm.Disconnect()
