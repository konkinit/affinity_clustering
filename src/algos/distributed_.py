import os
import sys
from itertools import groupby
from typing import List

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.utils import Graph


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

        return self.graph.getPartitions()

    def merge_nearest_neighbor(self, vertex: int) -> None:
        """Merge a vertex with its nearest neighbor

        Args:
            vertex (int): vertex
        """
        if vertex in self.merged:
            pass
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
