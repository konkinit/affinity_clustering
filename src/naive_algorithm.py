import sys
import math
import os
import heapq
import itertools



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""                      Helper functions                      """
"""                                                            """    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def load_data():
    return 0




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""                      Hierarchical Clustering Functions                       """
"""                                                                              """    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def euclidean_distance(data_point_one, data_point_two):
    """
    euclidean distance: https://en.wikipedia.org/wiki/Euclidean_distance
    assume that two data points have same dimension
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


def compute_pairwise_distance(dataset):
    result = []
    dataset_size = len(dataset)
    for i in range(dataset_size-1):    # ignore last i
        for j in range(i+1, dataset_size):     # ignore duplication
            dist = euclidean_distance(dataset[i]["data"], dataset[j]["data"])
            result.append( (dist, [dist, [[i], [j]]]) )
    return result


def compute_centroid(dataset, data_points_index):
    size = len(data_points_index)
    dim = len(dataset.columns)
    centroid = [0.0]*dim
    for idx in data_points_index:
        dim_data = dataset[idx]["data"]
        for i in range(dim):
            centroid[i] += float(dim_data[i])
    for i in range(dim):
        centroid[i] /= size
    return centroid



