import os
import sys
import findspark
from itertools import groupby
from math import ceil, log, floor
from pyspark import SparkContext, SparkConf
from simplejson import dump
from time import time
from typing import List

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.config import Distributed_Affinity_Params
from src.utils import Graph, getEdge, MST, partitioning_, partitioning__


findspark.init()


class Affinity:
    def __init__(self, graph_, k):
        self.k = k
        self.vertices = set()
        for e in graph_:
            self.vertices.add(e[0])
            self.vertices.add(e[1])
        self.edges = [(e[0], e[1], e[2]) for e in graph_]
        self.graph = Graph(self.vertices)
        self.nearest_neighbors = {}
        self.merged = set()

    def merge_nearest_neighbor(self, vertex: int) -> None:
        """Merge a vertex with its nearest neighbor

        Args:
            vertex (int): vertex
        """
        if vertex in self.merged:
            return
        if self.nearest_neighbors[self.nearest_neighbors[vertex]] == vertex:
            self.graph.merge(
                self.graph.getComponentRepr(vertex),
                self.graph.getComponentRepr(self.nearest_neighbors[vertex]),
            )
            self.merged.add(vertex)
            self.merged.add(self.nearest_neighbors[vertex])
        else:
            self.merge_nearest_neighbor(self.nearest_neighbors[vertex])
            self.graph.merge(
                self.graph.getComponentRepr(vertex),
                self.graph.getComponentRepr(self.nearest_neighbors[vertex]),
            )
            self.merged.add(vertex)
        return

    def clustering(self) -> List:
        """Compute clustering"""
        n_clusters = len(self.vertices)
        vertices_ = self.vertices
        while n_clusters > self.k:
            self.nearest_neighbors = {}
            self.merged = set()
            adjacency_matrix = []
            for e in self.edges:
                adjacency_matrix.append([e[0], e])
                adjacency_matrix.append([e[1], (e[1], e[0], e[2])])
            min_weight_edges = []
            for _, v_incident_edges in groupby(
                adjacency_matrix, lambda x: x[0]
            ):
                edge_group = [e[1] for e in v_incident_edges]
                min_weight_edges.append(min(edge_group, key=lambda x: x[2]))
            for e in min_weight_edges:
                self.nearest_neighbors[e[0]] = e[1]
            for v in vertices_:
                if v not in self.merged:
                    self.merge_nearest_neighbor(v)

            updated_edges = []
            for e in self.edges:
                if self.graph.getComponentRepr(
                    e[0]
                ) != self.graph.getComponentRepr(e[1]):
                    e_ = (
                        self.graph.getComponentRepr(e[0]),
                        self.graph.getComponentRepr(e[1]),
                        e[2],
                    )
                    updated_edges.append(e_)
            self.edges = updated_edges
            vertices_ = set(self.graph.getItems())
            n_clusters = len(self.graph.getItems())

        return self.graph.getPartitions()


class DistributedAffinity:
    def __init__(self, params: Distributed_Affinity_Params) -> None:
        conf = SparkConf()
        conf.setAppName(params.sc_name)
        self.sc = SparkContext(conf=conf)
        self.params = params
        self.clusters = []
        self.computation_time = 0.0
        self.k = params.k

    def compute(self) -> None:
        start = time()
        inp = self.sc.textFile(f"./data/inputs/{self.params.data_name}.txt")
        edges = inp.map(lambda x: getEdge(x))
        vertices = edges.flatMap(lambda x: [x[0], x[1]]).distinct()
        n = vertices.count()
        m = edges.count()
        eps = self.params.eps
        c = ceil(log(m)) / ceil(log(n)) - 1
        while c > eps:
            k = floor(n ** ((c - eps) / 2))
            c = ceil(log(m)) / ceil(log(n)) - 1
            keyedEdges = edges.map(lambda x: (x[0], x))
            half_partitioning = keyedEdges.groupByKey().flatMap(
                lambda x: partitioning_(x, k)
            )
            full_partionining = half_partitioning.groupByKey().flatMap(
                lambda x: partitioning__(x, k)
            )
            edges = full_partionining.groupByKey().flatMap(lambda x: MST(x[1]))
            m = edges.count()
        AF = Affinity(edges.collect(), self.k)
        clusters = AF.clustering()
        end = time()
        assert len(clusters) <= self.k
        self.computation_time = end - start
        self.clusters = clusters
        cluster_ = [f"Cluster_{str(i+1).zfill(2)}" for i in range(self.k)]
        cluster_dict = dict(zip(cluster_, clusters))
        with open(
            f"./data/outputs/{self.params.data_name}-distributed.json",
            "w"
        ) as f:
            dump(cluster_dict, f)
        f.close()
        return cluster_dict

    def inference(self) -> None:
        pass
