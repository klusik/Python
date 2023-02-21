"""
    Let's implement Dijkstra's search algorithm for connected nodes

    Author: Rudolf Klusal
"""

# IMPORTS #
import heapq


# RUNTIME #
def dijkstra(node_graph: dict, start_node: str, end_node: str) -> (list, int):
    """ Dijkstra's algorhitm
    @rtype: (list, list)
    @param node_graph: all nodes
    @param start_node: starting node
    @param end_node: end node
    @return: List of distances, list of nodes

    """
    # Initialize distance and predecessor dictionaries.
    # All nodes would be 'unvisited' and 'unknown,' so set
    # all nodes to 'inf' (means the highest value)
    distances = {
        node: float('inf') for node in node_graph
    }

    # Create predecessors dictionary with empty nodes
    # There would be the same nodes as in the input graph, just
    # not knowing any predecessors yet, so it would appear empty.
    predecessors = {
        node: None for node in node_graph
    }

    # Set distance of starting node to 0, because if we go from the start,
    # and we are on the start, the distance is zero.
    distances[start_node] = 0

    # Initialize heap with starting node and its distance.
    heap = [(0, start_node)]

    while heap:
        # Get node with the smallest distance from start. Heap automatically ensures that the top of heap
        # is the lowest. For next node we always need the node with smallest found distance from the start.
        curr_distance, current_node = heapq.heappop(heap)

        # If we've found the end node, construct path and return it.
        if current_node == end_node:
            # Create a placeholder for a final path.
            path_start_to_end_node = []

            # Go through all previous nodes (via predecessors) and save the path.
            # Go throught nodes similarily like when going through linked list, but backwards.
            while current_node is not None:
                path_start_to_end_node.append(current_node)
                current_node = predecessors[current_node]

            # Return reversed list for backward path (path is stored backward, so if we want
            # a path from start -> end and not backwards, it's necessary to order it).
            # Other value is the distance for the end node (the shortest path found).
            return path_start_to_end_node[::-1], distances[end_node]

        # If we haven't found the end node, update distances of neighbors.
        for neighbor, weight in node_graph[current_node].items():
            # Node distance to the next is the length of path to current node
            # plus the distance for the next node.
            node_distance = curr_distance + weight

            # If the distance to next node is less than distance previously found,
            # update it (find a minimum distance). Initial values are 'infinity,' so
            # if there's no previously found node distance, it's automatically true.
            if node_distance < distances[neighbor]:
                # Update node distance.
                distances[neighbor] = node_distance

                # Save from which node this update occured.
                predecessors[neighbor] = current_node

                # Save new node to heap (heap will automatically order nodes)
                heapq.heappush(heap, (node_distance, neighbor))

    # If we've exhausted all nodes and haven't found the end, return two empty lists. Just to be sure :-)
    return [], []


if __name__ == "__main__":
    graph = {
        'A': {'B': 5, 'C': 1},
        'B': {'A': 5, 'C': 2, 'D': 1},
        'C': {'A': 1, 'B': 2, 'D': 4, 'E': 8},
        'D': {'B': 1, 'C': 4, 'E': 3, 'F': 6},
        'E': {'C': 8, 'D': 3, 'F': 2, 'G': 3},
        'F': {'D': 6, 'E': 2, 'G': 1, 'H': 7},
        'G': {'E': 3, 'F': 1, 'H': 4},
        'H': {'F': 7, 'G': 4}
    }

    lukas_graph = {
        'A': {'B': 7, 'C': 50},
        'B': {'A': 7, 'C': 3, 'E': 13},
        'C': {'A': 50, 'B': 3, 'D': 1},
        'D': {'C': 1, 'E': 50, 'F': 15},
        'E': {'B': 13, 'D': 50, 'F': 101},
        'F': {'E': 101, 'D': 15},
    }

    graph_2 = {
        'A': {'B': 1, 'C': 2, 'D': 3},
        'B': {'A': 1, 'E': 2, 'F': 1},
        'C': {'A': 2, 'F': 1, 'G': 3},
        'D': {'A': 3, 'G': 2, 'H': 3},
        'E': {'B': 2, 'F': 1, 'I': 2},
        'F': {'B': 1, 'E': 1, 'J': 1, 'G': 1, 'C': 1},
        'G': {'F': 1, 'K': 2, 'L': 4, 'H': 2, 'D': 2, 'C': 3},
        'H': {'D': 3, 'G': 2, 'L': 1},
        'I': {'E': 2, 'J': 1, 'O': 3},
        'J': {'I': 1, 'P': 1, 'F': 1, 'E': 3},
        'K': {'G': 2, 'M': 3, 'L': 2},
        'L': {'K': 2, 'N': 3, 'H': 1, 'G': 4},
        'O': {'I': 3, 'P': 1, 'Q': 3},
        'P': {'J': 1, 'O': 1, 'Q': 2},
        'Q': {'O': 3, 'P': 2, 'T': 5},
        'M': {'K': 3, 'S': 2, 'N': 1},
        'N': {'L':3, 'M': 1, 'S': 2},
        'S': {'M': 2, 'N': 2, 'T': 4},
        'T': {'Q': 5, 'S': 4},
    }

    path, distance = dijkstra(graph_2, 'A', 'T')
    print(path)
    print(distance)
