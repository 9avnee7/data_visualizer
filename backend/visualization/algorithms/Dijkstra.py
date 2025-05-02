trace = []
import heapq

def dijkstra(graph, start):
    # Step 1: Initialize distances and priority queue
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]  # (distance, node)
    previous_nodes = {node: None for node in graph}  # Optional: for path reconstruction

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If current distance is greater than already found shortest distance, skip
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            # Relaxation step
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    trace.append({'event': 'completed', 'final_distances': dict(distance)})
    return distance, traces, previous_nodes


# Example graph: adjacency list format
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 5)],
    'C': [('A', 4), ('B', 2), ('D', 1)],
    'D': [('B', 5), ('C', 1)]
}

start_node = 'A'
distances, previous_nodes = dijkstra(graph, start_node)

# Output results
print("Shortest distances from start node:", distances)
print("Previous nodes for path tracing:", previous_nodes)
