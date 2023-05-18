import os
import sys
from itertools import groupby
from math import ceil, log, floor
from pyspark import SparkContext
from typing import List

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.utils import Graph, getEdge, MST


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

    def clustering(self) -> List:
        n_clusters = len(self.vertices)
        vertices_ = self.vertices.copy()
        while n_clusters > self.k:
            self.nearest_neighbors = {}
            self.merged = set()
            adjacency_matrix = []
            for e in self.edges:
                adjacency_matrix.append([e[0], e])
                adjacency_matrix.append([e[1], (e[1], e[0], e[2])])
            min_weight_edges = []
            for _, v_incident_edges in groupby(
                        adjacency_matrix, lambda x: x[0]):
                min_weight_edges.append(
                    min(v_incident_edges, key=lambda x: x[2])
                )
            for e in min_weight_edges:
                self.nearest_neighbors[e[0]] = e[1]
            for v in vertices_:
                if v not in self.merged:
                    self.merge_nearest_neighbor(v)

            updated_edges = []
            for e in self.edges:
                if self.graph.getComponentRepr(e[0]) != self.graph.getComponentRepr(e[1]):
                    e_ = (
                        self.graph.getComponentRepr(e[0]),
                        self.graph.getComponentRepr(e[1]),
                        e[2]
                    )
                    updated_edges.append(e_)
            self.edges = updated_edges
            self.vertices = set(self.graph.getItems())
            n_clusters = len(self.graph.getItems())

        return self.graph.getPartitions()

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


class DistributedAffinity:
    def __init__(self, params) -> None:
        self.sc = SparkContext(appName="Affinity")
        self.params = params

    def compute(self) -> List:
        inp = self.sc.textFile(self.params.inp_path)
        edges = inp.map(lambda x: getEdge(x))
        vertices = edges.flatMap(lambda x: [x[0], x[1]]).distinct()
        n = vertices.count()
        m = edges.count()
        eps = self.params.eps
        c = ceil(log(m))/ceil(log(n))-1
        while c > eps:
            k = floor(n**((c-eps)/2))
            c = ceil(log(m))/ceil(log(n))-1
            keyedEdges = edges.map(lambda x: (x[0], x))
            half_partitioning = keyedEdges.groupByKey().flatMap(lambda x: partitioning1(x, k))
            full_partionining = half_partitioning.groupByKey().flatMap(lambda x: partitioning2(x, k))
            edges = full_partionining.groupByKey().flatMap(lambda x: MST(x[1]))
            m = edges.count()
        AF = Affinity(edges.collect(), self.params.k)
        return AF.clustering()
