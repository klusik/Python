# Dijkstra Search

This project contains a validated Dijkstra implementation, a command-line interface, JSON graph examples, and a unit test suite.

## Usage

Run a single shortest-path query:

```bash
python3 dijkstra.py --graph examples/graph_02.json --start A --end T
```

Print distances and paths from one source to every node:

```bash
python3 dijkstra.py --graph examples/graph_01.json --start A --all
```

Run the tests:

```bash
python3 -m unittest discover -s tests -v
```

## Included examples

The repository already included two graph images. The matching JSON graphs now live in [examples/graph_01.json](/Users/klusik/Python/Bonusy/Dijkstra%20search/examples/graph_01.json) and [examples/graph_02.json](/Users/klusik/Python/Bonusy/Dijkstra%20search/examples/graph_02.json), so the visual examples and runnable input files stay aligned.

- `graph_01.png`
- `graph_02.png`
