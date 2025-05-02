trace = []
from collections import deque

def bfs(graph, start):
    # Create a queue for BFS and a set to track visited nodes
    queue = deque([start])
    trace.append({'event': 'init', 'start': start, 'queue': list(queue)})
    visited = set([start])
    
    # Start BFS traversal
    while queue:
        node = queue.popleft()
        trace.append({'event': 'dequeue', 'node': node, 'queue': list(queue)})  # Dequeue a node
        print(node, end=" ")    # Process the node (you can replace this with any operation)
        
        # Enqueue all unvisited neighbors
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# Example usage:
# Graph represented as an adjacency list (dictionary)
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Start BFS from node 'A'
bfs(graph, 'A')
