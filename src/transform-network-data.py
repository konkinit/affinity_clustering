import os
import sys

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.utils import getEdge


if __name__ == "__main__":
    with open("./data/inputs/rec-epinions.edges", "r") as f:
        graph = [getEdge(e.strip("\n")) for e in f.readlines()]
    f.close()

    with open("./data/inputs/OPINIONS-net.txt", "w") as f:
        for e in graph:
            f.write(f"{e[0]} {e[1]} {e[2]}\n")
    f.close()
