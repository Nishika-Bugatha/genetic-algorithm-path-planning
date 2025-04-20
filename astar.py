import heapq
from config import Config
from tools.draw_plot import define_links_dynamic

def a_star(start_index, goal_index):
    define_links_dynamic()
    graph = {i: [] for i in range(len(Config.path_points))}
    for a, b in Config.links:
        graph[a].append(b)

    def heuristic(a, b):
        p1, p2 = Config.path_points[a], Config.path_points[b]
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

    open_set = [(0, start_index, [])]
    visited = set()

    while open_set:
        cost, current, path = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        if current == goal_index:
            return path

        for neighbor in graph[current]:
            if neighbor not in visited:
                total_cost = cost + heuristic(current, neighbor) + heuristic(neighbor, goal_index)
                heapq.heappush(open_set, (total_cost, neighbor, path))

    return []
