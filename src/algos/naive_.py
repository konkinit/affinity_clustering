import os
import sys
from collections import OrderedDict
from heapq import heappop

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.config import Distributed_Affinity_Params
from src.utils import Graph, getEdge, MST, partitioning_, partitioning__


def hierarchical_clustering(dataset, num_clusters):
    """
    Main Process for hierarchical clustering

    """
    current_clusters = set_clusters(dataset)
    old_clusters = []
    heap = compute_distances(dataset)
    heap = build_priority_queue(heap)

    while len(current_clusters) > num_clusters:
        dist, min_item = heappop(heap)
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
    # current_clusters.sort()
    current_clusters = OrderedDict(current_clusters)
    final_clusts = {}
    for i, k in enumerate(current_clusters):
        final_clusts.setdefault("Cluster " + str(i + 1), k)
    return final_clusts
