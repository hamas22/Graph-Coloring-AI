import time

def is_safe(node, colour, graph, assignment):
    for neighbor in range(len(graph)):
        if graph[node][neighbor] == 1 and assignment[neighbor] == colour:
            return False
    return True

def dfs_order(graph, start):
    visited = set()
    order = []

    def dfs(node):
        visited.add(node)
        order.append(node)
        for neighbor in range(len(graph)):
            if graph[node][neighbor] == 1 and neighbor not in visited:
                dfs(neighbor)

    dfs(start)
    return order

def backtracking_colouring_core(graph, m, steps):
    n = len(graph)
    order = dfs_order(graph, 0)
    assignment = [-1] * n

    def solve(idx):
        if idx == len(order):
            return True

        node = order[idx]

        for colour in range(m):
            if is_safe(node, colour, graph, assignment):
                assignment[node] = colour
                steps.append(assignment.copy())

                if solve(idx + 1):
                    return True

                assignment[node] = -1
                steps.append(assignment.copy())

        return False

    if solve(0):
        return assignment
    else:
        return None

def find_optimal_backtracking(graph, max_colours):
    start_time = time.time()
    best_solution = None
    all_steps = []

    for m in range(1, max_colours + 1):
        current_steps = []
        solution = backtracking_colouring_core(graph, m, current_steps)
        if solution is not None:
            best_solution = solution
            all_steps.extend(current_steps)
            end_time = time.time()
            return best_solution, end_time - start_time, m, all_steps

    end_time = time.time()
    return None, end_time - start_time, max_colours, all_steps
