from dataclasses import dataclass


@dataclass(order=True, frozen=True)
class Node:
    gid: str
    loc: str
    ess: str
    ch: int

    def __str__(self):
        return f"{self.gid}"
