import time

# make sure if exist edge & not agjacent color
def is_safe(node, colour, graph, assignment):
    for neighbor in range(len(graph)):
        if graph[node][neighbor] == 1 and assignment[neighbor] == colour:
            return False
    return True


def backtracking_colouring(graph, m):
    n = len(graph)
    assignment = [-1] * n

    def solve(node):
        if node == n:
            return True
        for colour in range(m):
            if is_safe(node, colour, graph, assignment):
                assignment[node] = colour
                if solve(node + 1):
                    return True
                assignment[node] = -1
        return False

    start_time = time.time()
    if solve(0):
        end_time = time.time()
        return assignment, end_time - start_time
    else:
        end_time = time.time()
        return None, end_time - start_time
