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

# steps --> take number of colors
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

                #Recursion
                if solve(idx + 1):
                    return True

                assignment[node] = -1
                steps.append(assignment.copy())

        return False

    if solve(0):
        return assignment
    else:
        return None

# Minimize colors
# Try solve one color , 2 colors
def force_assign_with_conflicts(graph, m, steps):
    n = len(graph)
    assignment = [-1] * n
    for node in range(n):
        best_color = 0
        min_conflicts = float('inf')
        
        for color in range(m):
            current_conflicts = 0
            for neighbor in range(n):
                if graph[node][neighbor] == 1 and assignment[neighbor] == color:
                    current_conflicts += 1
            
            if current_conflicts < min_conflicts:
                min_conflicts = current_conflicts
                best_color = color
        
        assignment[node] = best_color
        steps.append(assignment.copy()) 
    
    return assignment

def find_optimal_backtracking(graph, max_colours):
    start_time = time.perf_counter()
    best_solution = None
    all_steps = []

    for m in range(1, max_colours + 1):
        current_steps = []
        solution = backtracking_colouring_core(graph, m, current_steps)
        if solution is not None:
            all_steps.extend(current_steps)
            end_time = time.perf_counter()
            return solution, end_time - start_time, m, all_steps
        else:
            all_steps.extend(current_steps)
    forced_steps = []
    best_solution = force_assign_with_conflicts(graph, max_colours, forced_steps)
    all_steps.extend(forced_steps)
    
    end_time = time.perf_counter()
    return best_solution, end_time - start_time, max_colours, all_steps