import subprocess
import sys
import unittest
from pathlib import Path

from dijkstra import dijkstra, dijkstra_all, load_graph


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DijkstraTests(unittest.TestCase):
    def test_unreachable_destination(self) -> None:
        graph = {
            "A": {"B": 1},
            "B": {"A": 1},
            "C": {},
        }

        result = dijkstra(graph, "A", "C")

        self.assertIsNone(result.path)
        self.assertEqual(float("inf"), result.distance)

    def test_missing_start_node(self) -> None:
        graph = {"A": {"B": 1}, "B": {"A": 1}}

        with self.assertRaisesRegex(ValueError, "Unknown start node"):
            dijkstra(graph, "Z", "A")

    def test_missing_end_node(self) -> None:
        graph = {"A": {"B": 1}, "B": {"A": 1}}

        with self.assertRaisesRegex(ValueError, "Unknown end node"):
            dijkstra(graph, "A", "Z")

    def test_neighbor_not_declared_in_graph(self) -> None:
        graph = {"A": {"B": 1}}

        with self.assertRaisesRegex(ValueError, "missing from the graph definition"):
            dijkstra(graph, "A", "B")

    def test_negative_edge_rejected(self) -> None:
        graph = {
            "A": {"B": -1},
            "B": {"A": -1},
        }

        with self.assertRaisesRegex(ValueError, "does not support negative weights"):
            dijkstra(graph, "A", "B")

    def test_non_numeric_weight_rejected(self) -> None:
        graph = {
            "A": {"B": "heavy"},
            "B": {},
        }

        with self.assertRaisesRegex(TypeError, "must be numeric"):
            dijkstra(graph, "A", "B")

    def test_start_equals_end(self) -> None:
        graph = {
            "A": {"B": 1},
            "B": {"A": 1},
        }

        result = dijkstra(graph, "A", "A")

        self.assertEqual(["A"], result.path)
        self.assertEqual(0.0, result.distance)
        self.assertEqual(0.0, result.distances["A"])

    def test_multiple_equal_cost_paths(self) -> None:
        graph = {
            "A": {"B": 1, "C": 1},
            "B": {"A": 1, "D": 1},
            "C": {"A": 1, "D": 1},
            "D": {"B": 1, "C": 1},
        }

        result = dijkstra(graph, "A", "D")

        self.assertEqual(2.0, result.distance)
        self.assertIn(result.path, [["A", "B", "D"], ["A", "C", "D"]])

    def test_all_shortest_paths_from_one_source(self) -> None:
        graph = load_graph(PROJECT_ROOT / "examples" / "graph_02.json")

        result = dijkstra_all(graph, "A")

        self.assertEqual(9.0, result.distances["T"])
        self.assertEqual(["A", "B", "F", "G", "K", "M", "S", "T"], result.path_to("T"))

    def test_cli_single_path(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(PROJECT_ROOT / "dijkstra.py"),
                "--graph",
                str(PROJECT_ROOT / "examples" / "graph_02.json"),
                "--start",
                "A",
                "--end",
                "T",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        self.assertIn("Path: A -> B -> F -> G -> K -> M -> S -> T", completed.stdout)
        self.assertIn("Distance: 9", completed.stdout)

    def test_cli_all_distances(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(PROJECT_ROOT / "dijkstra.py"),
                "--graph",
                str(PROJECT_ROOT / "examples" / "graph_01.json"),
                "--start",
                "A",
                "--all",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        self.assertIn("Start: A", completed.stdout)
        self.assertIn("H: distance=14, path=A -> C -> B -> D -> E -> G -> H", completed.stdout)


if __name__ == "__main__":
    unittest.main()
