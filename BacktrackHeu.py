import time

def graph_colouring_optimized(graph, max_colours):
    n = len(graph)
    assignment = [-1] * n
    steps = []

    # Degree heuristic
    degrees = [sum(row) for row in graph]

    def available_colours(node):
        used = {assignment[neighbor] for neighbor in range(n) if graph[node][neighbor] == 1 and assignment[neighbor] != -1}
        return [c for c in range(max_colours) if c not in used]

    def available_colours_lcv(node):
        colours = available_colours(node)
        # LCV
        def constraining_value(colour):
            count = 0
            for neighbor in range(n):
                if graph[node][neighbor] == 1 and assignment[neighbor] == -1:
                    if colour in available_colours(neighbor):
                        count += 1
            return count
        return sorted(colours, key=constraining_value)

    def select_node():
        # MRV
        unassigned = [i for i in range(n) if assignment[i] == -1]
        if not unassigned:
            return None
        mrv_min = min(len(available_colours(i)) for i in unassigned)
        candidates = [i for i in unassigned if len(available_colours(i)) == mrv_min]
        # Degree Heuristic: اختر العقدة ذات أكبر درجة عند التعادل
        return max(candidates, key=lambda x: degrees[x])

    def solve():
        node = select_node()
        if node is None:
            return True

        for colour in available_colours_lcv(node):
            assignment[node] = colour
            steps.append(assignment.copy())

            # Forward Checking
            if all(available_colours(neighbor) for neighbor in range(n) if graph[node][neighbor] == 1 and assignment[neighbor] == -1):
                if solve():
                    return True

            assignment[node] = -1  # Backtrack
            steps.append(assignment.copy())

        return False

    start_time = time.time()
    best_solution = None
    chromatic_number = None

    for m in range(1, max_colours + 1):
        assignment = [-1] * n
        steps.clear()
        if solve():
            best_solution = assignment.copy()
            chromatic_number = m
            break

    end_time = time.time()
    return best_solution, chromatic_number, steps, end_time - start_time
