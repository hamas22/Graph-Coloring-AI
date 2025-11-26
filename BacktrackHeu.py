import time

def get_current_state(graph, assignment):
    n = len(graph)
    state = [-1] * n
    for node, color in assignment.items():
        state[node] = color
    return state

# Get order of nodes using DFS
def dfs_order(graph, start):
    visited = set()
    order = []

    # Trace graph
    def dfs(node):
        visited.add(node)
        order.append(node)
        for neigh in graph[node]:
            if neigh not in visited:
                dfs(neigh)

    dfs(start)
    return order

# Get MRV
def mrv_with_degree(current_node, assignment, domains, graph):
    # Get child of current node that not assigned
    children = [n for n in graph[current_node] if n not in assignment]

    # Check if all assigned
    if not children:
        return None
    
    # Check if only one node not assigned
    if len(children) == 1:
        return children[0]

    # Get smallest domain size
    min_domain = min(len(domains[n]) for n in children)

    # All nodes that share that domain size
    candidates = [n for n in children if len(domains[n]) == min_domain]

    # If only one return it
    if len(candidates) == 1:
        return candidates[0]

    # else using degree heuristic (choose node with greatest neighbors)
    return max(candidates, key=lambda n: len([x for x in graph[n] if x not in assignment]))

# Get LCV
def lcv_order_values(node, domains, graph, assignment):
    # Count number of occurance for each color
    def constraint_count(color):
        return sum(color in domains[neigh] for neigh in graph[node] if neigh not in assignment)
    
    # Return sorted list in ascending order
    return sorted(domains[node], key=constraint_count)

# Forward Checking
def forward_check(node, color, domains, graph, assignment):
    # Var for store color remove (used for backtracking later)
    removed = []

    # Remove color from all neighbors
    for neigh in graph[node]:
        if neigh not in assignment and color in domains[neigh]:
            domains[neigh].remove(color)
            removed.append((neigh, color))

            # Check empty list (backtracking case)
            if len(domains[neigh]) == 0:
                return False, removed

    return True, removed

# Restore color that removed from nodes (backtrack)
def restore_domains(removed, domains):
    for neigh, color in removed:
        domains[neigh].add(color)

# Solve
def dfs_backtracking(graph, domains, assignment, current_node, steps):
    # If all nodes assigned exit (back all recursive and return assignment)
    if len(assignment) == len(graph):
        return assignment

    # Select next node using MRV
    node = mrv_with_degree(current_node, assignment, domains, graph)

    # Check if node not null
    if node is None:
        return None

    # Sort colors using LCV and loop on it
    for color in lcv_order_values(node, domains, graph, assignment):
        # Initially assign color into node
        assignment[node] = color

        steps.append(get_current_state(graph, assignment))
        # ====================================

        # Run forward checking
        ok, removed = forward_check(node, color, domains, graph, assignment)

        # Check for backtracking
        if ok:
            result = dfs_backtracking(graph, domains, assignment, node, steps)
            if result:
                return result  # success

        # Backtrack
        restore_domains(removed, domains)
        del assignment[node]

        steps.append(get_current_state(graph, assignment))
        # ========================================

    return None  # no solution

# Minimize number of colored assigned
def solve_graph_coloring(graph, num_colors, start):
    # Create start time var (to keep track of time)
    start_time = time.time()
    
    max_colors = 0 

    # Add list that include all colors
    domains = {node: set(range(1, num_colors + 1)) for node in graph}

    # Create assignment and steps var (keep track of steps and node assigned)
    assignment = {}
    steps = []

    # Start DFS from start node and record it
    assignment[start] = min(domains[start])
    
    steps.append(get_current_state(graph, assignment))
    # ================================

    # Check color validation
    ok, removed = forward_check(start, assignment[start], domains, graph, assignment)
    if ok:
        result = dfs_backtracking(graph, domains, assignment, start, steps)
        if result:
            # Ceate end time var
            end_time = time.time()

            # Get number of colors
            max_colors = max(result.values())
            
            return list(result.values()), end_time - start_time, max_colors, steps

    # Backtrack
    restore_domains(removed, domains)
    del assignment[start]

    steps.append(get_current_state(graph, assignment))
    # =================================

    # Ceate end time var
    end_time = time.time()
    
    return None, end_time - start_time, max_colors, steps