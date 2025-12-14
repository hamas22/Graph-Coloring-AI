import time

def force_assign_optimized(graph, m, steps):
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
        domains_snapshot = {i: [best_color] if i == node else list(range(m)) for i in range(n)}
        steps.append((assignment.copy(), domains_snapshot))
    return assignment

def graph_colouring_optimized(graph, max_colours):
    n = len(graph)
    degrees = [sum(row) for row in graph]
    final_assignment = None
    final_steps = []
    min_chromatic = 0
    
    def fast_domain_copy(domains):
        return {k: v[:] for k, v in domains.items()}

    def select_unassigned_variable(assignment, domains):
        unassigned = [v for v in range(n) if assignment[v] == -1]
        if not unassigned:
            return -1
        return min(unassigned, key=lambda v: (len(domains[v]), -degrees[v]))

    def calculate_constraining_power(node, color, assignment, domains, n):
        count = 0
        for neighbor in range(n):
            if graph[node][neighbor] == 1 and assignment[neighbor] == -1:
                if color in domains[neighbor]:
                    count += 1
        return count

    def solve(assignment, domains, steps):
        if -1 not in assignment:
            return True

        node = select_unassigned_variable(assignment, domains)
        
        sorted_colors = sorted(
            domains[node][:], 
            key=lambda color: calculate_constraining_power(node, color, assignment, domains, n)
        )

        for color in sorted_colors:
            assignment[node] = color
            steps.append((assignment[:], fast_domain_copy(domains)))

            new_domains = fast_domain_copy(domains)
            possible = True
            
            for neighbor in range(n):
                if graph[node][neighbor] == 1 and assignment[neighbor] == -1:
                    if color in new_domains[neighbor]:
                        new_domains[neighbor].remove(color)
                        if not new_domains[neighbor]:
                            possible = False
                            break
            
            if possible:
                if solve(assignment, new_domains, steps):
                    return True

            assignment[node] = -1
            steps.append((assignment[:], fast_domain_copy(domains)))

        return False

    start_time = time.perf_counter()

    found = False
    for m in range(1, max_colours + 1):
        assignment = [-1] * n
        domains = {i: list(range(m)) for i in range(n)}
        steps = []
        
        if solve(assignment, domains, steps):
            final_assignment = assignment
            final_steps = steps
            min_chromatic = m
            found = True
            break
        
        final_steps = steps

    if not found:
        forced_steps = []
        final_assignment = force_assign_optimized(graph, max_colours, forced_steps)
        final_steps.extend(forced_steps)
        min_chromatic = max_colours

    end_time = time.perf_counter()
    
    return final_assignment, min_chromatic, final_steps, end_time - start_time