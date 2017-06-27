#/usr/bin/env python
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

s = range(1000000)

src = rank - 1 if rank != 0 else size - 1
dst = rank + 1 if rank != size - 1 else 0

# This may work because the data is small
comm.send(s[:10], dest=dst)
m = comm.recv(source=src)
print rank, m

# This doesn't work because the data is large
if False:
    comm.send(s, dest=dst)
    m = comm.recv(source=src)
    print rank, m[:10]

# This works
if rank % 2 == 0:
    comm.send(s, dest=dst)
    m = comm.recv(source=src)
else:
    m = comm.recv(source=src)
    comm.send(s, dest=dst)

print rank, m[:10]
