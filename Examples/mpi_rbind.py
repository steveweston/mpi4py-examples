#!/usr/bin/env python
import numpy as np
from mpi4py import MPI

def rbind(comm, x):
    return np.vstack(comm.allgather(x))

def rbind2(comm, x):
    size = comm.Get_size()
    m = np.zeros((size, len(x)), dtype=np.int)
    comm.Allgather([x, MPI.INT], [m, MPI.INT])
    return m

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    x = np.arange(4, dtype=np.int) * rank

    a = rbind(comm, x)
    if rank == 0:
        print(a)

    b = rbind2(comm, x)
    if rank == 0:
        print(b)

    assert a.shape == b.shape
    assert (a == b).all()
