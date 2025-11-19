import time

def solve_forward_checking_core(graph, m, steps):
    n = len(graph)
    assignment = [-1] * n
    domain = [set(range(m)) for _ in range(n)]
    
    def update_domains(node, colour, current_domain):
        new_domain = [d.copy() for d in current_domain]
        
        for neighbor in range(n):
            if graph[node][neighbor] == 1 and assignment[neighbor] == -1:
                if colour in new_domain[neighbor]:
                    new_domain[neighbor].remove(colour)
                    
                    if not new_domain[neighbor]:
                        return None
        return new_domain

    def solve(node, current_domain):
        if node == n:
            return True
        
        steps.append((assignment.copy(), [list(d) for d in current_domain]))
        
        for colour in sorted(list(current_domain[node])):
            assignment[node] = colour
            
            next_domain = update_domains(node, colour, current_domain)
            
            if next_domain is not None:
                if solve(node + 1, next_domain):
                    return True
            
            assignment[node] = -1
            steps.append((assignment.copy(), [list(d) for d in current_domain]))

        return False

    if solve(0, domain):
        steps.append((assignment.copy(), [list(d) for d in domain]))
        return assignment
    else:
        return None

def find_optimal_forward_checking(graph, max_colours):
    start_time = time.time()
    n = len(graph)
    best_solution = None
    all_steps = []
    
    for m in range(1, max_colours + 1):
        current_steps = []
        solution = solve_forward_checking_core(graph, m, current_steps)
        
        if solution is not None:
            best_solution = solution
            all_steps.extend(current_steps)
            end_time = time.time()
            return best_solution, end_time - start_time, m, all_steps
    
    end_time = time.time()
    return None, end_time - start_time, max_colours, all_steps