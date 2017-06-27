#/usr/bin/env python
from mpi4py import MPI
import numpy as np
import random

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if size == 0:
    sys.exit(0)

while True:
    dice = comm.allgather(random.randint(1, 1000))
    sender = dice.index(max(dice))
    receiver = dice.index(min(dice))
    if sender != receiver:
        break
    if rank == 0:
        print 'Trying again:', dice

if rank == sender:
    print dice
    m = np.arange(100, dtype=np.float64).reshape(10, 10)
    comm.Send([m[2,:], MPI.DOUBLE], dest=receiver)
elif rank == receiver:
    x = np.zeros((10, 10), dtype=np.float64)
    comm.Recv([x[2,:], MPI.DOUBLE])
    print x
