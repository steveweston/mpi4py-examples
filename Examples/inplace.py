#!/usr/bin/env python
import numpy as np
from mpi4py import MPI

def islice(n, chunks):
    i = 0
    j = 0
    while chunks > 0:
        q, r = divmod(n, chunks)
        q += r > 0
        j += q
        yield slice(i, j)
        i = j
        n -= q
        chunks -= 1

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    x = np.zeros((6,7), dtype=np.int32)
    nr, nc = x.shape
    slices = list(islice(nr, size))
    cnt = [nc * (s.stop - s.start) for s in slices]
    dsp = [nc * s.start for s in slices]
    x[slices[rank],:] = rank
    comm.Allgatherv(MPI.IN_PLACE, [x, (cnt, dsp), MPI.INT])
    if rank == 0:
        print(slices)
        print(cnt)
        print(dsp)
        print(x)
