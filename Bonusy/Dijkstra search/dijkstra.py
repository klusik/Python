"""Validated Dijkstra shortest-path utilities and a small CLI.

The module exposes two main entry points:

- ``dijkstra_all()`` computes the shortest-path tree from one start node.
- ``dijkstra()`` computes the shortest path between one start and one end node.

Graphs are represented as adjacency mappings of the form
``{"A": {"B": 5, "C": 1}, "B": {"A": 5}}``.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
import heapq
from numbers import Real
from pathlib import Path
from typing import Final, Optional, TypeAlias

Node: TypeAlias = str
Weight: TypeAlias = float
DistanceMap: TypeAlias = dict[Node, Weight]
PredecessorMap: TypeAlias = dict[Node, Optional[Node]]
GraphInput: TypeAlias = dict[Node, dict[Node, Real]]
Graph: TypeAlias = dict[Node, dict[Node, Weight]]

INF: Final[float] = float("inf")

__all__ = [
    "Graph",
    "GraphInput",
    "ShortestPathResult",
    "ShortestPathTree",
    "dijkstra",
    "dijkstra_all",
    "format_path",
    "load_graph",
    "validate_graph",
]


@dataclass(frozen=True)
class ShortestPathTree:
    """Shortest-path data computed from one start node.

    Attributes:
        start: The source node from which distances were computed.
        distances: Shortest known distance from ``start`` to every node.
            Unreachable nodes keep ``INF``.
        predecessors: Previous node on the shortest path to each node.
            The start node and unreachable nodes map to ``None``.
    """

    start: Node
    distances: DistanceMap
    predecessors: PredecessorMap

    def path_to(self, target: Node) -> Optional[list[Node]]:
        """Return the shortest path from ``start`` to ``target``.

        Args:
            target: Destination node whose path should be reconstructed.

        Returns:
            A list of nodes from ``start`` to ``target`` when reachable,
            otherwise ``None``.

        Raises:
            ValueError: If ``target`` is not present in the validated graph.
        """
        if target not in self.distances:
            raise ValueError(f"Unknown target node: {target!r}")

        if self.distances[target] == INF:
            return None

        path: list[Node] = []
        current_node: Optional[Node] = target

        # Rebuild the path by walking predecessor links backwards
        # from the target to the start node.
        while current_node is not None:
            path.append(current_node)
            current_node = self.predecessors[current_node]

        path.reverse()
        return path

    def reachable_nodes(self) -> list[Node]:
        """Return nodes whose shortest-path distance is finite."""
        return [
            node for node, distance in self.distances.items()
            if distance < INF
        ]


@dataclass(frozen=True)
class ShortestPathResult:
    """Shortest-path result for one concrete ``start -> end`` query.

    Attributes:
        start: Source node supplied by the caller.
        end: Destination node supplied by the caller.
        path: Ordered nodes from ``start`` to ``end`` or ``None`` when unreachable.
        distance: Total cost of ``path`` or ``INF`` when unreachable.
        distances: Full shortest-distance map from ``start`` to every node.
        predecessors: Predecessor links used to reconstruct paths.
    """

    start: Node
    end: Node
    path: Optional[list[Node]]
    distance: Weight
    distances: DistanceMap
    predecessors: PredecessorMap


def validate_graph(node_graph: GraphInput) -> Graph:
    """Validate and normalize a graph before running Dijkstra's algorithm.

    Validation is intentionally strict so the search loop can assume a clean,
    fully declared graph:

    - every node name must be a string
    - every adjacency list must be a dictionary
    - every edge weight must be numeric and non-negative
    - every referenced neighbor must also exist as a top-level node

    Args:
        node_graph: Raw adjacency mapping supplied by the caller.

    Returns:
        A normalized graph whose weights are converted to ``float``.

    Raises:
        TypeError: If the graph shape or weight types are invalid.
        ValueError: If a weight is negative or a neighbor is undeclared.
    """
    if not isinstance(node_graph, dict):
        raise TypeError("Graph must be a dict[str, dict[str, float]].")

    normalized_graph: Graph = {}

    for node, neighbors in node_graph.items():
        if not isinstance(node, str):
            raise TypeError(f"Graph node names must be strings, got {type(node).__name__}.")
        if not isinstance(neighbors, dict):
            raise TypeError(f"Neighbors for node {node!r} must be a dictionary.")

        normalized_graph[node] = {}
        for neighbor, weight in neighbors.items():
            if not isinstance(neighbor, str):
                raise TypeError(
                    f"Neighbor names for node {node!r} must be strings, "
                    f"got {type(neighbor).__name__}."
                )
            if not isinstance(weight, Real):
                raise TypeError(
                    f"Weight from {node!r} to {neighbor!r} must be numeric, "
                    f"got {type(weight).__name__}."
                )
            if weight < 0:
                raise ValueError(
                    f"Dijkstra's algorithm does not support negative weights: "
                    f"{node!r} -> {neighbor!r} = {weight}."
                )
            normalized_graph[node][neighbor] = float(weight)

    # Ensure the graph is closed over its node set so lookups in the hot path
    # never need defensive existence checks.
    for node, neighbors in normalized_graph.items():
        for neighbor in neighbors:
            if neighbor not in normalized_graph:
                raise ValueError(
                    f"Neighbor {neighbor!r} referenced by {node!r} is missing "
                    "from the graph definition."
                )

    return normalized_graph


def dijkstra_all(node_graph: GraphInput, start_node: Node) -> ShortestPathTree:
    """Compute shortest paths from one start node to every node in the graph.

    Args:
        node_graph: Graph represented as adjacency mappings.
        start_node: Source node from which all distances are computed.

    Returns:
        A ``ShortestPathTree`` containing distances and predecessor links.
    """
    graph = validate_graph(node_graph)

    return _dijkstra_all_validated(graph, start_node)


def _dijkstra_all_validated(graph: Graph, start_node: Node) -> ShortestPathTree:
    """Compute shortest paths from an already validated graph."""

    if start_node not in graph:
        raise ValueError(f"Unknown start node: {start_node!r}")

    distances: DistanceMap = {node: INF for node in graph}
    predecessors: PredecessorMap = {node: None for node in graph}
    distances[start_node] = 0.0
    heap: list[tuple[Weight, Node]] = [(0.0, start_node)]

    while heap:
        current_distance, current_node = heapq.heappop(heap)

        # Skip stale queue entries left behind by previous relaxations.
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            candidate_distance = current_distance + weight
            # Relaxation step: only update a neighbor when the newly discovered
            # route is strictly better than the best route found so far.
            if candidate_distance < distances[neighbor]:
                distances[neighbor] = candidate_distance
                predecessors[neighbor] = current_node
                heapq.heappush(heap, (candidate_distance, neighbor))

    return ShortestPathTree(
        start=start_node,
        distances=distances,
        predecessors=predecessors,
    )


def dijkstra(
    node_graph: GraphInput,
    start_node: Node,
    end_node: Node,
) -> ShortestPathResult:
    """Compute the shortest path between one start node and one end node.

    Args:
        node_graph: Graph represented as adjacency mappings.
        start_node: Source node.
        end_node: Destination node.

    Returns:
        A ``ShortestPathResult`` with the concrete path, its total cost, and
        the full single-source distance/predecessor maps.
    """
    graph = validate_graph(node_graph)

    if start_node not in graph:
        raise ValueError(f"Unknown start node: {start_node!r}")
    if end_node not in graph:
        raise ValueError(f"Unknown end node: {end_node!r}")

    if start_node == end_node:
        distances: DistanceMap = {node: INF for node in graph}
        predecessors: PredecessorMap = {node: None for node in graph}
        distances[start_node] = 0.0
        return ShortestPathResult(
            start=start_node,
            end=end_node,
            path=[start_node],
            distance=0.0,
            distances=distances,
            predecessors=predecessors,
        )

    tree = _dijkstra_all_validated(graph, start_node)
    return ShortestPathResult(
        start=start_node,
        end=end_node,
        path=tree.path_to(end_node),
        distance=tree.distances[end_node],
        distances=tree.distances,
        predecessors=tree.predecessors,
    )


def load_graph(graph_path: str | Path) -> Graph:
    """Load, validate, and normalize a graph from a JSON file."""
    with Path(graph_path).open("r", encoding="utf-8") as graph_file:
        loaded_graph = json.load(graph_file)
    return validate_graph(loaded_graph)


def format_path(path: Optional[list[Node]]) -> str:
    """Format a path for human-readable CLI output."""
    if path is None:
        return "unreachable"
    return " -> ".join(path)


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser for the CLI."""
    parser = argparse.ArgumentParser(description="Run Dijkstra shortest-path search.")
    parser.add_argument("--graph", required=True, help="Path to a JSON graph file.")
    parser.add_argument("--start", required=True, help="Start node.")
    parser.add_argument("--end", help="End node for a single shortest-path query.")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Print distances and paths from the start node to every node.",
    )
    return parser


def main() -> int:
    """Run the command-line interface and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.all and args.end is None:
        parser.error("--end is required unless --all is used.")

    graph = load_graph(args.graph)

    if args.all:
        tree = dijkstra_all(graph, args.start)
        print(f"Start: {tree.start}")
        for node in sorted(tree.distances):
            distance = tree.distances[node]
            distance_label = "inf" if distance == INF else f"{distance:g}"
            print(
                f"{node}: distance={distance_label}, path={format_path(tree.path_to(node))}"
            )
        return 0

    result = dijkstra(graph, args.start, args.end)
    distance_label = "inf" if result.distance == INF else f"{result.distance:g}"
    print(f"Path: {format_path(result.path)}")
    print(f"Distance: {distance_label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
