#/usr/bin/env python
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    m = np.array(range(50), dtype=np.float64)
    for dest in range(size):
        if dest != rank:
            comm.Send([m, MPI.DOUBLE], dest=dest, tag=100 + dest)
else:
    info = MPI.Status()
    comm.Probe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=info)

    n = info.Get_elements(MPI.DOUBLE)
    src = info.Get_source()
    tag = info.Get_tag()

    x = np.empty(n, dtype=np.float64)
    comm.Recv([x, MPI.DOUBLE], source=src, tag=tag)
    print x
