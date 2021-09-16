from collections import namedtuple
import heapq
from queue import PriorityQueue

GraphNode = namedtuple("GraphNode", ["name", "neighbors", "distance"])
JudgedNode = namedtuple("JudgedNode", ["score", "name", "weight", "path_through"])


def a_star(graph, start_point, end_point):
    q = PriorityQueue()
    start = graph[start_point]
    start_node = JudgedNode(start.distance, start.name, 0, 0)
    q.put(start_node)
    processed = []

    while True:
        node = q.get()

        # end if final node is 1st in queue
        if node.name == end_point:
            break

        # iterate over neighbors
        for neighbor, weight in graph[node.name].neighbors.items():
            in_processed = False
            for proc_node in processed:
                if proc_node.name == neighbor:
                    in_processed = True

            # if neighbor is already processed, ignore it
            if not in_processed:
                neighbor_node = graph[neighbor]

                weight_to_node = node.weight + weight
                score = weight_to_node + neighbor_node.distance

                jn = JudgedNode(score, neighbor, weight_to_node, node.name)

                # if node is already in queue, compare scores and delete already existing if needed
                for idx, n in enumerate(q.queue):
                    if n.name == neighbor and score < n.score:
                        del q.queue[idx]
                        heapq.heapify(q.queue)
                        break

                q.put(jn)

        processed.append(node)

    # append final node
    processed.append(node)

    for path_node in processed:
        if path_node.name == end_point:
            next = path_node
            break

    result = []
    while next.name != start_point:
        result.append(next.name)

        for path_node in processed:
            if path_node.name == next.path_through:
                next = path_node
                break

    result.append(next.name)
    result.reverse()

    return result
