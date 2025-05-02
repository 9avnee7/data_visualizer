export const addDijkstraTrace = (modifiedCode) => {
    // Trace 1: After initializing the queue
    modifiedCode = modifiedCode.replace(
      /heapq\.heappush\(pq, \(0, start\)\)/,
      `heapq.heappush(pq, (0, start))\n    trace.append({'event': 'init', 'start': start, 'distances': dict(distances)})`
    );
  
    // Trace 2: After popping from the queue
    modifiedCode = modifiedCode.replace(
      /curr_dist, curr_node = heapq\.heappop\(pq\)/,
      `curr_dist, curr_node = heapq.heappop(pq)\n        trace.append({'event': 'pop', 'node': curr_node, 'queue': list(pq), 'distances': dict(distances)})`
    );
  
    // Trace 3: Skipped node due to visited
    modifiedCode = modifiedCode.replace(
      /if curr_node in visited:\n\s+continue/,
      `if curr_node in visited:\n        trace.append({'event': 'skip', 'node': curr_node})\n        continue`
    );
  
    // Trace 4: When marking a node as visited
    modifiedCode = modifiedCode.replace(
      /visited\.add\(curr_node\)/,
      `visited.add(curr_node)\n        trace.append({'event': 'visit', 'node': curr_node})`
    );
  
    // Trace 5: Before checking condition to relax edge
    modifiedCode = modifiedCode.replace(
      /if distances\[neighbor\] > distances\[curr_node\] \+ weight:/,
      `if distances[neighbor] > distances[curr_node] + weight:\n                trace.append({'event': 'check_relax', 'from': curr_node, 'to': neighbor, 'existing': distances[neighbor], 'candidate': distances[curr_node] + weight})`
    );
  
    // Trace 6: After pushing to the queue
    modifiedCode = modifiedCode.replace(
      /heapq\.heappush\(pq, \(distances\[neighbor\], neighbor\)\)/,
      `heapq.heappush(pq, (distances[neighbor], neighbor))\n                trace.append({'event': 'relaxed', 'from': curr_node, 'to': neighbor, 'new_distance': distances[neighbor], 'queue': list(pq)})`
    );
  
    // Trace 7: Final trace
    modifiedCode = modifiedCode.replace(
      /return distances/,
      `trace.append({'event': 'completed', 'final_distances': dict(distances)})\n    return distances, trace`
    );
  
    return modifiedCode;
  };
  



export const addBFSTrace = (modifiedCode) => {
    // Initialize trace array if not present
    if (!modifiedCode.includes('trace = []')) {
        modifiedCode = modifiedCode.replace(
            /def bfs\(.*\)\s*:/,
            'def bfs(graph, start):\n    trace = []'
        );
    }

    const replacements = [
        {
            pattern: /queue\s*=\s*(?:deque\()?\[start\]\)?/,
            replacement: 'queue = deque([start])\n    trace.append({"event": "init", "start": start, "queue": list(queue)})'
        },
        {
            pattern: /node\s*=\s*queue\.popleft\(\)/,
            replacement: 'node = queue.popleft()\n        trace.append({"event": "dequeue", "node": node, "queue": list(queue)})'
        },
        {
            pattern: /if node in visited:\n\s*continue/,
            replacement: 'if node in visited:\n        trace.append({"event": "skip", "node": node})\n        continue'
        },
        {
            pattern: /visited\.add\(node\)/,
            replacement: 'visited.add(node)\n        trace.append({"event": "visit", "node": node, "visited": list(visited)})'
        },
        {
            pattern: /queue\.append\(neighbor\)/,
            replacement: 'queue.append(neighbor)\n            trace.append({"event": "enqueue", "from": node, "to": neighbor, "queue": list(queue)})'
        },
        {
            pattern: /return visited/,
            replacement: 'trace.append({"event": "completed", "visited_order": list(visited)})\n    return visited, trace'
        }
    ];

    replacements.forEach(({pattern, replacement}) => {
        modifiedCode = modifiedCode.replace(pattern, replacement);
    });

    return modifiedCode;
};

export const addDFSTrace = (modifiedCode) => {
    if (!modifiedCode.includes('trace = []')) {
        modifiedCode = modifiedCode.replace(
            /def dfs\(.*\)\s*:/,
            'def dfs(graph, start):\n    trace = []'
        );
    }

    const replacements = [
        {
            pattern: /stack\s*=\s*\[start\]/,
            replacement: 'stack = [start]\n    trace.append({"event": "init", "start": start, "stack": list(stack)})'
        },
        {
            pattern: /node\s*=\s*stack\.pop\(\)/,
            replacement: 'node = stack.pop()\n        trace.append({"event": "pop", "node": node, "stack": list(stack)})'
        },
        {
            pattern: /if node in visited:/,
            replacement: 'if node in visited:\n        trace.append({"event": "skip", "node": node})'
        },
        {
            pattern: /visited\.add\(node\)/,
            replacement: 'visited.add(node)\n        trace.append({"event": "visit", "node": node, "visited": list(visited)})'
        },
        {
            pattern: /stack\.append\(neighbor\)/,
            replacement: 'stack.append(neighbor)\n            trace.append({"event": "push", "from": node, "to": neighbor, "stack": list(stack)})'
        },
        {
            pattern: /return visited/,
            replacement: 'trace.append({"event": "completed", "visited_order": list(visited)})\n    return visited, trace'
        }
    ];

    replacements.forEach(({pattern, replacement}) => {
        modifiedCode = modifiedCode.replace(pattern, replacement);
    });

    return modifiedCode;
};


export const addMergeSortTrace = (modifiedCode) => {
    if (!modifiedCode.includes('trace = []')) {
        modifiedCode = modifiedCode.replace(
            /def mergeSort\(.*\)\s*:/,
            'def mergeSort(arr):\n    trace = []'
        );
    }

    const replacements = [
        {
            pattern: /def mergeSort\(arr\):/,
            replacement: 'def mergeSort(arr):\n    trace.append({"event": "init", "arr": arr.copy()})'
        },
        {
            pattern: /mid\s*=\s*len\(arr\)\s*\/\/\s*2/,
            replacement: 'mid = len(arr) // 2\n    trace.append({"event": "split", "arr": arr.copy(), "left": arr[:mid], "right": arr[mid:]})'
        },
        {
            pattern: /mergeSort\(arr\[:mid\]\)/,
            replacement: 'mergeSort(arr[:mid])\n    trace.append({"event": "recursive_left", "arr": arr[:mid]})'
        },
        {
            pattern: /mergeSort\(arr\[mid:\]\)/,
            replacement: 'mergeSort(arr[mid:])\n    trace.append({"event": "recursive_right", "arr": arr[mid:]})'
        },
        {
            pattern: /while i < len\(L\) and j < len\(R\):/,
            replacement: 'while i < len(L) and j < len(R):\n        trace.append({"event": "merge", "L": L.copy(), "R": R.copy(), "i": i, "j": j, "result": result.copy()})'
        },
        {
            pattern: /result\.append\(L\[i\]\)/,
            replacement: 'result.append(L[i])\n        trace.append({"event": "append_left", "value": L[i], "result": result.copy()})'
        },
        {
            pattern: /result\.append\(R\[j\]\)/,
            replacement: 'result.append(R[j])\n        trace.append({"event": "append_right", "value": R[j], "result": result.copy()})'
        },
        {
            pattern: /return result/,
            replacement: 'trace.append({"event": "completed", "sorted_array": result.copy()})\n    return result, trace'
        }
    ];

    replacements.forEach(({pattern, replacement}) => {
        modifiedCode = modifiedCode.replace(pattern, replacement);
    });

    return modifiedCode;
};

export const addQuickSortTrace = (modifiedCode) => {
    if (!modifiedCode.includes('trace = []')) {
        modifiedCode = modifiedCode.replace(
            /def quickSort\(.*\)\s*:/,
            'def quickSort(arr):\n    trace = []'
        );
    }

    const replacements = [
        {
            pattern: /def quickSort\(arr\):/,
            replacement: 'def quickSort(arr):\n    trace.append({"event": "init", "arr": arr.copy()})'
        },
        {
            pattern: /pivot\s*=\s*arr\[low\]/,
            replacement: 'pivot = arr[low]\n    trace.append({"event": "pivot_selected", "pivot": pivot, "arr": arr.copy()})'
        },
        {
            pattern: /i\s*=\s*low\s*-\s*1/,
            replacement: 'i = low - 1\n    trace.append({"event": "partition_start", "arr": arr.copy(), "low": low, "high": high})'
        },
        {
            pattern: /for j in range\(low, high\):/,
            replacement: 'for j in range(low, high):\n        trace.append({"event": "compare", "i": i, "j": j, "pivot": pivot, "current": arr[j]})'
        },
        {
            pattern: /arr\[i\], arr\[j\]\s*=\s*arr\[j\], arr\[i\]/,
            replacement: 'arr[i], arr[j] = arr[j], arr[i]\n        trace.append({"event": "swap", "i": i, "j": j, "arr": arr.copy()})'
        },
        {
            pattern: /arr\[i\s*\+\s*1\], arr\[high\]\s*=\s*arr\[high\], arr\[i\s*\+\s*1\]/,
            replacement: 'arr[i + 1], arr[high] = arr[high], arr[i + 1]\n    trace.append({"event": "partition_end", "pivot_position": i + 1, "arr": arr.copy()})'
        },
        {
            pattern: /quickSort\(arr, low, i\)/,
            replacement: 'quickSort(arr, low, i)\n    trace.append({"event": "recursive_left", "low": low, "high": i, "arr": arr.copy()})'
        },
        {
            pattern: /quickSort\(arr, i\s*\+\s*2, high\)/,
            replacement: 'quickSort(arr, i + 2, high)\n    trace.append({"event": "recursive_right", "low": i + 2, "high": high, "arr": arr.copy()})'
        },
        {
            pattern: /return arr/,
            replacement: 'trace.append({"event": "completed", "sorted_array": arr.copy()})\n    return arr, trace'
        }
    ];

    replacements.forEach(({pattern, replacement}) => {
        modifiedCode = modifiedCode.replace(pattern, replacement);
    });

    return modifiedCode;
};