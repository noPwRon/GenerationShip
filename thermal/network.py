"""
network.py
-----------
Stub module for thermal network modeling.

Responsible for:
    - Defining node/edge abstractions for conductive and radiative exchange.
    - Loading material properties via thermal.materials.
    - Providing helpers that higher-level simulations can consume.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ThermalNode:
    """Simple placeholder for a lumped thermal node."""

    node_id: str
    capacity_kj_per_k: float = 0.0
    temperature_c: float = 20.0


@dataclass
class ThermalEdge:
    """Placeholder conductive edge between two thermal nodes."""

    from_node: str
    to_node: str
    conductance_kw_per_k: float = 0.0


class ThermalNetwork:
    """Minimal skeleton until full solver lands."""

    def __init__(self) -> None:
        self.nodes: Dict[str, ThermalNode] = {}
        self.edges: List[ThermalEdge] = []

    def add_node(self, node: ThermalNode) -> None:
        self.nodes[node.node_id] = node

    def add_edge(self, edge: ThermalEdge) -> None:
        self.edges.append(edge)

    def summary(self) -> Dict[str, int]:
        """Return counts of nodes and edges for quick diagnostics."""

        return {"nodes": len(self.nodes), "edges": len(self.edges)}
