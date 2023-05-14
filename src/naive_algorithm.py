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



def hierarchical_clustering(dataset, num_clusters):
    """
    Main Process for hierarchical clustering

    """
    current_clusters = []
    old_clusters = []
    heap = compute_distances(dataset)
    heap = build_priority_queue(heap)

    while len(current_clusters) > num_clusters:
        dist, min_item = heapq.heappop(heap)
        # pair_dist = min_item[0]
        pair_data = min_item[1]

        # judge if include old cluster
        if not valid_heap_node(min_item, old_clusters):
            continue

        new_cluster = {}
        new_cluster_elements = sum(pair_data, [])
        new_cluster_cendroid = compute_centroid(dataset, new_cluster_elements)
        new_cluster_elements.sort()
        new_cluster.setdefault("centroid", new_cluster_cendroid)
        new_cluster.setdefault("elements", new_cluster_elements)
        for pair_item in pair_data:
            old_clusters.append(pair_item)
            del current_clusters[str(pair_item)]
        add_heap_entry(heap, new_cluster, current_clusters)
        current_clusters[str(new_cluster_elements)] = new_cluster
    current_clusters.sort()
    return current_clusters


def build_priority_queue(distance_list):
    heapq.heapify(distance_list)
    heap = distance_list
    return heap

def valid_heap_node(heap_node, old_clusters):
    #pair_dist = heap_node[0]
    pair_data = heap_node[1]
    for old_cluster in old_clusters:
        if old_cluster in pair_data:
            return False
    return True

def add_heap_entry(heap, new_cluster, current_clusters):
    for ex_cluster in current_clusters.values():
        new_heap_entry = []
        dist = euclidean_distance(ex_cluster["centroid"], new_cluster["centroid"])
        new_heap_entry.append(dist)
        new_heap_entry.append([new_cluster["elements"], ex_cluster["elements"]])
        heapq.heappush(heap, (dist, new_heap_entry))





