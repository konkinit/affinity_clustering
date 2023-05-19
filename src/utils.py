from itertools import combinations
from math import sqrt, log
from heapq import heapify, heappush
import numpy as np
from random import randrange
from typing import List, Union


def set_clusters(dataset):
    """Initialize clusters"""
    clusters = {}
    n = len(dataset)
    for i in range(n):
        clusters_key = str([i])
        clusters.setdefault(clusters_key, {})
        clusters[clusters_key].setdefault("centroid", dataset[i])
        clusters[clusters_key].setdefault("elements", [i])
    return clusters


def build_priority_queue(distance_list):
    """Build the priority queue"""
    heapify(distance_list)
    heap = distance_list
    return heap


def valid_heap_node(heap_node, old_clusters):
    pair_data = heap_node[1]
    for old_cluster in old_clusters:
        if old_cluster in pair_data:
            return False
    return True


def add_heap_entry(heap, new_cluster, current_clusters):
    for ex_cluster in current_clusters.values():
        new_heap_entry = []
        dist = euclidean_distance(
            ex_cluster["centroid"],
            new_cluster["centroid"]
        )
        new_heap_entry.append(dist)
        new_heap_entry.append(
            [new_cluster["elements"], ex_cluster["elements"]]
        )
        heappush(heap, (dist, new_heap_entry))


def euclidean_distance(data_point_one, data_point_two):
    """Evaluate the euclidean distance with assumption"""
    assert len(data_point_one) == len(data_point_two)
    size = len(data_point_one)
    result = 0.0
    for i in range(size):
        f1 = float(data_point_one[i])
        f2 = float(data_point_two[i])
        tmp = f1 - f2
        result += pow(tmp, 2)
    result = sqrt(result)
    return result


def compute_distances(dataset):
    """Compute pairwise distance"""
    result = []
    dataset_size = len(dataset)
    for i in range(dataset_size - 1):  # ignore last i
        for j in range(i + 1, dataset_size):  # ignore duplication
            dist = euclidean_distance(dataset[i], dataset[j])
            result.append((dist, [dist, [[i], [j]]]))
    return result


def compute_centroid(dataset, data_points_index):
    """Compute cetroid"""
    size = len(data_points_index)
    dim = int(np.shape(dataset)[1])
    centroid = [0.0] * dim
    for idx in data_points_index:
        dim_data = dataset[idx]
        for i in range(dim):
            centroid[i] += float(dim_data[i])
    for i in range(dim):
        centroid[i] /= size
    return centroid


def getMetadataSats(graph):
    """Get graph metadat infos"""
    vertices = set()
    for e in graph:
        vertices.add(getEdge(e)[0])
        vertices.add(getEdge(e)[1])
    n = len(vertices)
    m = len(graph)
    c = log(m) / log(n) - 1
    return n, m, c


def getEdge(edge_str: str) -> List:
    """Represent an edge in a list format from
    its string format

    Args:
        edge_str (str): edge representation in string

    Returns:
        List: edge represented in a list where the 2 first
        elements denote the vertoices and the last elmnt
        the weight
    """
    edge_ = edge_str.split(" ")
    return [int(edge_[0]), int(edge_[1]), float(edge_[2])]


class Graph:
    """A graph instance"""
    def __init__(self, vertices: Union[set, list]) -> None:
        self.items = dict((v, [v]) for v in vertices)
        self.num_vertices = dict((v, 1) for v in vertices)
        self.component_repr = dict((v, v) for v in vertices)

    def merge(self, u_: int, v_: int) -> None:
        """Merge the components containing u_ and v_

        Args:
            u_ (int): a vertex representator
            v_ (int): a vertex representator
        """
        u, v = min(u_, v_), max(u_, v_)
        for node in self.items[u]:
            self.component_repr[node] = v
            self.items[v].append(node)
        self.num_vertices[v] += self.num_vertices[u]
        del self.num_vertices[u]
        del self.items[u]

    def getComponentRepr(self, v: int) -> int:
        """Get the reprensatator of the component of
        which vertex v belongs

        Args:
            v (int): vertex

        Returns:
            int: component representator
        """
        return self.component_repr[v]

    def getItems(self) -> List:
        """Get the graph vertices

        Returns:
            List: list of vertices
        """
        return list(self.items.keys())

    def getPartitions(self) -> List[list]:
        """Get the partition of the graph

        Returns:
            List[list]: list of partitions
        """
        return list(self.items.values())


def MST(graph: List[list]) -> List[tuple]:
    """Return the Minimum Spanning Tree edges
    from the graph

    Args:
        graph (List[list]): the graph in an (?, 3) dim array
        type where for each row the first two cols and last
        col represent respectively the vertices and the
        associated weights

    Returns:
        List[Tuple]: minimum spanning tree
    """
    MST = []
    edges = sorted([(e[0], e[1], e[2]) for e in graph], key=lambda x: x[2])
    vertices = set()
    for e in edges:
        vertices.add(e[0])
        vertices.add(e[1])
    graph_ = Graph(vertices)
    for e in edges:
        e1_component = graph_.getComponentRepr(e[0])
        e2_component = graph_.getComponentRepr(e[1])

        if e1_component != e2_component:
            MST.append(e)
            graph_.merge(e1_component, e2_component)
    return MST


def partitioning_(x: List, k: int):
    edges = x[1]
    out = []
    partitionId = randrange(0, k)
    for e in edges:
        out.append((e[1], (partitionId, e)))
    return out


def partitioning__(x: List, k: int):
    edges = x[1]
    out = []
    partitionId = randrange(0, k)
    for e in edges:
        firstPartiton = e[0]
        edge = e[1]
        out.append(((firstPartiton, partitionId), edge))
    return out


def tabular2network(dataset_name: str) -> None:
    """Read a tabular dataset and convert it to network dataset
    """
    with open(f"./data/inputs/{dataset_name}-tab.txt", "r") as f:
        graph = list(
            map(
                lambda x: list(map(float, x)),
                [e.strip("\n").split(" ") for e in f.readlines()],
            )
        )
    f.close()

    with open(f"./data/inputs/{dataset_name}-net.txt", "w") as file:
        for i in range(len(graph) - 1):
            for j in range(i + 1, len(graph)):
                dij = round(euclidean_distance(graph[i], graph[j]), 3)
                file.write(f"{i+1} {j+1} {dij}\n")
    file.close()


def check_pair_togetherness(u: int, v: int, partitions: List):
    """Check if two pair of vertices are in the same
    cluster given a clustering outputs
    """
    togetherness = 0
    for cluster in partitions:
        togetherness += int((u in cluster) & (v in cluster))
    return togetherness


def rand_index(
        V: Union[list, set],
        X: List[list],
        Y: List[list]
) -> float:
    """Evaluate the rand index score

    Args:
        V (Union[list, set]): vertices
        X (List[list]): a clustering of V
        Y (List[list]): a clustering of V

    Returns:
        float: the rand index value
    """
    n = len(V)
    a, b = 0, 0
    edges = list(combinations(V, 2))
    for e in edges:
        a += check_pair_togetherness(e[0], e[1], X)
        b += check_pair_togetherness(e[0], e[1], Y)
    return (2*(a+b))/(n*(n-1))
