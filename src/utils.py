from typing import List, Union


def getEdge(edge_str: str) -> List:
    """Represents an edge in a list format from
    its string format

    Args:
        edge_str (str): edge representation in string

    Returns:
        List: edge represented in a list where the 2 first
        elements denote the vertoices and the last elmnt
        the weight
    """
    edge_ = edge_str.split(',')
    return [edge_.u, edge_.v, edge_.weight]


class Graph:
    """a graph initialisator
    """
    def __init__(
            self,
            vertices: Union[set, list]
    ) -> None:
        self.items = dict((v, [v]) for v in vertices)
        self.size = dict((v, 1) for v in vertices)
        self.component_repr = dict((v, v) for v in vertices)

    def merge(
            self,
            u_: Union[int, float, str],
            v_: Union[int, float, str]
    ) -> None:
        """Merge the components containing u_ and v_

        Args:
            u_ (Union[int, float, str]): a vertex representator
            v_ (Union[int, float, str]): a vertex representator
        """
        u, v = min(u_, v_), max(u_, v_)
        for node in self.items[u]:
            self.component_repr[node] = v
            self.items[v].append(node)
        self.size[v] += self.size[u]
        del self.size[u]
        del self.items[u]

    def getComponentRepr(
            self,
            v: Union[int, float, str]
    ) -> Union[int, float, str]:
        """Get the reprensatator of the component of
        which vertex v belongs

        Args:
            v (Union[int, float, str]): vertex

        Returns:
            Union[int, float, str]: component representator
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
        graph (List[list]): he graph in an (?, 3) dim array type
        where for each row the first two cols and last col
        represent respectively the vertices and the weights

    Returns:
        List[Tuple]: minimum spanning tree
    """
    MST = []
    edges = sorted(
        [(e[0], e[1], e[2]) for e in graph],
        key=lambda x: x[2]
    )
    vertices = set()
    for e in edges:
        vertices.add(e[0])
        vertices.add(e[1])
    graph_ = Graph(vertices)
    for e in edges:
        e1_component = graph_.getComponent(e[0])
        e2_component = graph_.getComponent(e[1])

        if e1_component != e2_component:
            MST.append(e)
            graph_.merge(e1_component, e2_component)
    return MST
