const algorithmTemplates = {
    dijkstra: {
      algorithm: "Dijkstra",
      template: [
        {
          event: "init",
          description: "Initialization of the algorithm",
          required_fields: {
            start: "string (starting node)",
            distances: "object (initial distances to all nodes)",
            queue: "array (initial priority queue)",
            visited: "array (initially empty)"
          }
        },
        {
          event: "visit",
          description: "When a node is being processed",
          required_fields: {
            node: "string (current node being visited)",
            distance: "number (current shortest distance to node)",
            distances: "object (current distances to all nodes)",
            queue: "array (current state of priority queue)",
            visited: "array (currently visited nodes)"
          }
        },
        {
          event: "check_relax",
          description: "Before checking if edge relaxation is needed",
          required_fields: {
            from: "string (source node)",
            to: "string (target neighbor node)",
            current_distance: "number (distance to current node)",
            edge_weight: "number (weight of the edge)",
            old_distance: "number (previous distance to neighbor)",
            new_distance: "number (potential new distance)",
            will_update: "boolean (whether relaxation will occur)"
          }
        },
        {
          event: "relax",
          description: "After updating a node's distance",
          required_fields: {
            from: "string (source node)",
            to: "string (target neighbor node)",
            new_distance: "number (updated distance)",
            distances: "object (updated distances to all nodes)",
            queue: "array (updated priority queue)"
          }
        },
        {
          event: "complete",
          description: "When algorithm finishes",
          required_fields: {
            final_distances: "object (all shortest distances)",
            paths: "object (previous nodes for path reconstruction)"
          }
        }
      ]
    },
  
    bfs: {
      algorithm: "BFS",
      template: [
        {
          event: "init",
          description: "Initialization of the algorithm",
          required_fields: {
            start: "string (starting node)",
            queue: "array (initial queue containing start node)",
            visited: "array (initially empty)"
          }
        },
        {
          event: "enqueue",
          description: "When a node is added to the queue",
          required_fields: {
            node: "string (node being enqueued)",
            queue: "array (current state of queue)",
            visited: "array (currently visited nodes)"
          }
        },
        {
          event: "dequeue",
          description: "When a node is processed from the queue",
          required_fields: {
            node: "string (node being processed)",
            queue: "array (queue after dequeue)",
            visited: "array (updated visited nodes)"
          }
        },
        {
          event: "neighbor_check",
          description: "When checking a neighbor node",
          required_fields: {
            current: "string (node being processed)",
            neighbor: "string (neighbor being checked)",
            visited: "array (current visited nodes)"
          }
        },
        {
          event: "complete",
          description: "When algorithm finishes",
          required_fields: {
            visited: "array (all visited nodes in BFS order)"
          }
        }
      ]
    },
  
    dfs: {
      algorithm: "DFS",
      template: [
        {
          event: "init",
          description: "Initialization of the algorithm",
          required_fields: {
            start: "string (starting node)",
            stack: "array (initial stack containing start node)",
            visited: "array (initially empty)"
          }
        },
        {
          event: "push",
          description: "When a node is pushed to the stack",
          required_fields: {
            node: "string (node being pushed)",
            stack: "array (current state of stack)",
            visited: "array (currently visited nodes)"
          }
        },
        {
          event: "pop",
          description: "When a node is processed from the stack",
          required_fields: {
            node: "string (node being processed)",
            stack: "array (stack after pop)",
            visited: "array (updated visited nodes)"
          }
        },
        {
          event: "neighbor_check",
          description: "When checking a neighbor node",
          required_fields: {
            current: "string (node being processed)",
            neighbor: "string (neighbor being checked)",
            visited: "array (current visited nodes)"
          }
        },
        {
          event: "complete",
          description: "When algorithm finishes",
          required_fields: {
            visited: "array (all visited nodes in DFS order)"
          }
        }
      ]
    },
  
    merge: {
      algorithm: "Merge Sort",
      template: [
        {
          event: "init",
          description: "Initialization of the algorithm",
          required_fields: {
            array: "array (initial unsorted array)"
          }
        },
        {
          event: "split",
          description: "When the array is being split",
          required_fields: {
            parent_array: "array (original array being split)",
            left_half: "array (left portion)",
            right_half: "array (right portion)"
          }
        },
        {
          event: "merge",
          description: "When two halves are being merged",
          required_fields: {
            left: "array (left half being merged)",
            right: "array (right half being merged)",
            merged: "array (result after merging)"
          }
        },
        {
          event: "compare",
          description: "When comparing two elements",
          required_fields: {
            elements: "array (pair of elements being compared)",
            result: "string (which element is smaller)"
          }
        },
        {
          event: "complete",
          description: "When algorithm finishes",
          required_fields: {
            sorted_array: "array (final sorted array)"
          }
        }
      ]
    },
  
    quick: {
      algorithm: "Quick Sort",
      template: [
        {
          event: "init",
          description: "Initialization of the algorithm",
          required_fields: {
            array: "array (initial unsorted array)"
          }
        },
        {
          event: "partition",
          description: "When partitioning the array",
          required_fields: {
            array: "array (current subarray being partitioned)",
            pivot: "number (selected pivot value)",
            left: "array (elements less than pivot)",
            right: "array (elements greater than pivot)"
          }
        },
        {
          event: "pivot_select",
          description: "When selecting a pivot",
          required_fields: {
            array: "array (current subarray)",
            pivot: "number (selected pivot value)",
            pivot_index: "number (index of pivot)"
          }
        },
        {
          event: "swap",
          description: "When swapping two elements",
          required_fields: {
            elements: "array (pair of elements being swapped)",
            indices: "array (indices of swapped elements)",
            array: "array (state after swap)"
          }
        },
        {
          event: "complete",
          description: "When algorithm finishes",
          required_fields: {
            sorted_array: "array (final sorted array)"
          }
        }
      ]
    }
  };
  
  // Example usage:
  // const dijkstraTemplate = algorithmTemplates.dijkstra;
  // const bfsTemplate = algorithmTemplates.bfs;
  
  module.exports = algorithmTemplates;