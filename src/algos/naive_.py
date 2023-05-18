import os
import sys
from collections import OrderedDict
from heapq import heappop
from simplejson import dump
from time import time

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.config import Naive_Algo_Params
from src.utils import (
    set_clusters,
    build_priority_queue,
    valid_heap_node,
    add_heap_entry,
    compute_distances,
    compute_centroid,
)


class NaiveHierarchical:
    def __init__(self, params: Naive_Algo_Params) -> None:
        self.params = params
        self.k = params.k
        self.computation_time = 0.0

    def compute(self):
        """Compute hierarchical clustering naively
        """
        with open(f"./data/inputs/{self.params.data_name}.txt", "r") as f:
            graph = list(map(
                lambda x: list(map(float, x)),
                [e.strip("\n").split(" ") for e in f.readlines()]
            ))
        f.close()
        current_clusters = set_clusters(graph)
        old_clusters = []
        heap = compute_distances(graph)
        heap = build_priority_queue(heap)
        start = time()
        while len(current_clusters) > self.k:
            _, min_item = heappop(heap)
            pair_data = min_item[1]
            # judge if include old cluster
            if not valid_heap_node(min_item, old_clusters):
                continue

            new_cluster = {}
            new_cluster_elements = sum(pair_data, [])
            new_cluster_cendroid = compute_centroid(
                graph,
                new_cluster_elements
            )
            new_cluster_elements.sort()
            new_cluster.setdefault("centroid", new_cluster_cendroid)
            new_cluster.setdefault("elements", new_cluster_elements)
            for pair_item in pair_data:
                old_clusters.append(pair_item)
                del current_clusters[str(pair_item)]
            add_heap_entry(heap, new_cluster, current_clusters)
            current_clusters[str(new_cluster_elements)] = new_cluster
        end = time()
        self.computation_time = end - start
        current_clusters = OrderedDict(current_clusters)
        final_clusts = {}
        for i, clust in enumerate(current_clusters):
            final_clusts.setdefault("Cluster " + str(i+1).zfill(2), clust)
        with open(
            f"./data/outputs/{self.params.data_name.split('-')[0]}-naive.json",
            "w"
        ) as f:
            dump(final_clusts, f)
        f.close()

        return final_clusts
