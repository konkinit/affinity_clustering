import sys
import math
import os
import heapq
import itertools
import numpy as np
from sklearn import datasets


# Importing iris dataset for tests 
iris = datasets.load_iris()
data = iris['data']


# Tests naive Hierarchical clustering functions
# euclidean distance 
sys.path.append('.')
from src.naive_algorithm import euclidean_distance
from src.naive_algorithm import compute_distances
from src.naive_algorithm import compute_centroid

print(euclidean_distance(data[0], data[1]))
print(euclidean_distance(data[2], data[3]))
print(euclidean_distance(data[15], data[22]))
print()

# compute distances 
dist = compute_distances(data)
print(dist[:6])
print()

# compute centroid 
centr1 = compute_centroid(data, [12, 18, 109, 1, 22, 16, 149])
centr2 = compute_centroid(data, [100, 0, 2, 78, 25, 93, 122])
print(centr1)
print(centr2)


#set clusters 
from src.naive_algorithm import set_clusters
print(set_clusters(data[:10]))
print()

#Test hierarchical clustering 
from src.naive_algorithm import hierarchical_clustering
res = hierarchical_clustering(data, 3)
print(res)