from typing import List, Tuple, Set, Union


class GraphUtils:
    def __init__(self, vertices: Union[Set, List]) -> None:
        self.items = dict((v, [v]) for v in vertices)
        self.size = dict((v, 1) for v in vertices)
        self.component_representant = dict((v, v) for v in vertices)

    def merge(
            self,
            u: Union[int, float, str],
            v: Union[int, float, str]
    ) -> None:
        """Merge the components containing u and v

        Args:
            u (Union[int, float, str]): a vertex representator
            v (Union[int, float, str]): a vertex representator
        """
        for node in self.items[u]:
            self.component_representant[node] = v
            self.items[v].append(node)
        self.size[v] += self.size[u]
        del self.size[u]
        del self.items[v]

    def getComponentRepresentant(
            self,
            v: Union[int, float, str]
    ) -> Union[int, float, str]:
        """Get the reprensatator of the component of
        which vertex v belongs

        Args:
            v (Union[int, float, str]): _description_

        Returns:
            Union[int, float, str]: component representator
        """
        return self.component_representant[v]

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


def MST(graph: List[list]) -> List[Tuple]:
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
    edges = sorted([(e[0], e[1], e[2]) for e in graph], key=lambda x: x[2])
    vertices = set()
    for e in edges:
        vertices.add(e[0])
        vertices.add(e[1])
    graph_ = GraphUtils(vertices)
    for e in edges:
        e1_component = graph_.getComponent(e[0])
        e2_component = graph_.getComponent(e[1])

        if e1_component != e2_component:
            MST.append(e)
            graph_.merge(e1_component, e2_component)
    return MST
