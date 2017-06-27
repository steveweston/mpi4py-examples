#/usr/bin/env python
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

n = 1000000
s = np.empty(n, dtype=np.float64)
s[:] = rank
r = np.zeros(n, dtype=np.float64)

src = rank - 1 if rank != 0        else size - 1
dst = rank + 1 if rank != size - 1 else 0

MPI.Request.Waitall([
    comm.Isend(s, dest=dst),
    comm.Irecv(r, source=src)
])
print rank, r[:10]
