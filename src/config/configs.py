from dataclasses import dataclass


@dataclass
class Distributed_Affinity_Params:
    data_name: str
    k: int
    eps: float = 0.05
