#/usr/bin/env python
from mpi4py import MPI
import numpy as np
import random

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

dice = comm.allgather(random.randint(1, 1000))
sender = dice.index(max(dice))

if rank == sender:
    print dice
    m = np.array(range(50), dtype=np.float64)
    for dest in range(size):
        if dest != rank:
            comm.Send([m, 30, MPI.DOUBLE], dest=dest, tag=100 + dest)
else:
    x = np.zeros((100,), dtype=np.float64)
    info = MPI.Status()
    comm.Recv([x, MPI.DOUBLE], source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG,
              status=info)

    print 'Bytes:    ', info.Get_count()
    print 'Elements: ', info.Get_elements(MPI.DOUBLE)
    print 'Source:   ', info.Get_source()
    print 'Tag:      ', info.Get_tag()
    print x
