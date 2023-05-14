class Affinity:
    def __init__(self, graph, k):
        self.k = k
        self.vertices = set()
        for e in graph:
            self.vertices.append(e[0])
            self.vertices.append(e[1])
        self.edges = [[e[0], e[1], e[2]] for e in graph]
