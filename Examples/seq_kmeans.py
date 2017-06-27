#!/usr/bin/env python
import sys
import numpy as np
from scipy.cluster.vq import kmeans, whiten

obs = whiten(np.genfromtxt('data.csv', dtype=float, delimiter=','))
centers = 10
nstart = 100 if len(sys.argv) == 1 else int(sys.argv[1])
np.random.seed(0)  # for testing purposes
centroids, distortion = kmeans(obs, centers, nstart)
print('Best distortion for %d tries: %f' % (nstart, distortion))
