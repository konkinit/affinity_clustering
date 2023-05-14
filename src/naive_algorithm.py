import sys
import sys
import math
import os
import heapq
import itertools
import numpy as np



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""                      Helper functions                      """
"""                                                            """    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def load_data():
    return 0


def display(current_clusters):
    clusters = current_clusters.values()
    for cluster in clusters:
        cluster["elements"].sort()
        print(cluster["elements"])


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""                      Hierarchical Clustering Functions                       """
"""                                                                              """    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def euclidean_distance(data_point_one, data_point_two):
    """
    euclidean distance: assume that two data points have same dimension
    """
    size = len(data_point_one)
    result = 0.0
    for i in range(size):
        f1 = float(data_point_one[i])   # feature for data one
        f2 = float(data_point_two[i])   # feature for data two
        tmp = f1 - f2
        result += pow(tmp, 2)
    result = math.sqrt(result)
    return result


def compute_distances(dataset):
    result = []
    dataset_size = len(dataset)
    for i in range(dataset_size-1):    # ignore last i
        for j in range(i+1, dataset_size):     # ignore duplication
            dist = euclidean_distance(dataset[i], dataset[j])
            result.append( (dist, [dist, [[i], [j]]]) )
    return result


def compute_centroid(dataset, data_points_index):
    size = len(data_points_index)
    dim = int(np.shape(dataset)[1])
    centroid = [0.0]*dim
    for idx in data_points_index:
        dim_data = dataset[idx]
        for i in range(dim):
            centroid[i] += float(dim_data[i])
    for i in range(dim):
        centroid[i] /= size
    return centroid







