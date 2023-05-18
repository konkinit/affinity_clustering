from dataclasses import dataclass


@dataclass
class Distributed_Affinity_Params:
    sc_name: str
    data_name: str
    k: int
    eps: float = 0.05


@dataclass
class Naive_Algo_Params:
    k: int
