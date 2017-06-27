#!/usr/bin/env python
import sys
import numpy as np
from scipy.cluster.vq import kmeans, whiten
from operator import itemgetter
from math import ceil
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
np.random.seed(seed=rank)  # XXX should use parallel RNG

obs = whiten(np.genfromtxt('data.csv', dtype=float, delimiter=','))

centers = 10
nstart = 100 if len(sys.argv) == 1 else int(sys.argv[1])
n = int(ceil(float(nstart) / size))
centroids, distortion = kmeans(obs, centers, n)

results = comm.gather((centroids, distortion), root=0)
if rank == 0:
    assert len(results) == size
    print('Worker distortions:', [r[1] for r in results])
    results.sort(key=itemgetter(1))
    result = results[0]
    print('Best distortion for %d tries: %f' % (nstart, result[1]))
else:
    assert results is None
