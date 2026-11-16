from collections import deque
from heapq import heappush, heappop 

def shortest_shortest_path(graph, source):
    """
    Params: 
      graph.....a graph represented as a dict where each key is a vertex
                and the value is a set of (vertex, weight) tuples (as in the test case)
      source....the source node
      
    Returns:
      a dict where each key is a vertex and the value is a tuple of
      (shortest path weight, shortest path number of edges). See test case for example.
    """
    # Dijkstra, but the heap key is (weight, edges) so ties go to fewer edges
    def helper(visited, frontier):
        if len(frontier) == 0:
            return visited
        weight, edges, v = heappop(frontier)
        if v in visited:
            return helper(visited, frontier)
        visited[v] = (weight, edges)
        for u, w in graph[v]:
            heappush(frontier, (weight + w, edges + 1, u))
        return helper(visited, frontier)

    frontier = []
    heappush(frontier, (0, 0, source))
    return helper(dict(), frontier)
    
