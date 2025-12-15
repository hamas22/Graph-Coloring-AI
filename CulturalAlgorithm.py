

# import random
# import time
# class CulturalAlgorithm:
#     def __init__(self, graph, population_size=20, generations=50, mutation_rate=0.1, max_colours=4):
#         self.graph = graph


#         # عدد الأفراد في كل جيل 
#          # if 10 or 20 Excution fast & Solve weak
#          # if 100 or 200 solve vareity & long time
#          # لو الجراف كبير نستخدم رقم كبير 
#         self.population_size = population_size


#          # عدد الأجيال 
#          # if small --> fast but stop before get the best solution
#          # if big --> maybe get the best solution but long time

#         self.generations = generations



#         # if 0.01 the evolve weak 
#         # if 0.1 good balance 
#         # if 0.5 many variety <-- algo is random & not learn good

#         self.mutation_rate = mutation_rate
#         self.max_colours = max_colours
#         self.n = len(graph)
#         self.situational_knowledge = None
#         # self.normative_knowledge = {}

#     def fitness(self, individual):
#         conflicts = 0
#         for i in range(self.n):
#             if individual[i] == -1: continue # تجنب العقد غير الملونة إن وجدت
#             for j in range(i + 1, self.n):
#                 if self.graph[i][j] == 1 and individual[i] == individual[j]:
#                     conflicts += 1
        
#         used_colors = len(set(c for c in individual if c != -1))
        
#         return conflicts * 1000 + used_colors

#     def create_individual(self):
#         return [random.randint(0, self.max_colours - 1) for _ in range(self.n)]

#     def mutate(self, individual):
#         if random.random() < self.mutation_rate:
#             idx = random.randint(0, self.n - 1)
#             individual[idx] = random.randint(0, self.max_colours - 1)
#         return individual

#     def crossover(self, p1, p2):
#         point = random.randint(1, self.n - 1)
#         # Slicing is faster than creating new loops
#         child = p1[:point] + p2[point:]
#         return child

#     def evolve(self):
#         start_time = time.perf_counter() 

#         population = [self.create_individual() for _ in range(self.population_size)]
#         steps_history = []
        
#         best_fitness_overall = float('inf')

#         for generation in range(self.generations):
#             population.sort(key=self.fitness)
            
#             best_in_gen = population[0]
#             current_fitness = self.fitness(best_in_gen)

#             # تحديث أفضل حل (Situational Knowledge)
#             if self.situational_knowledge is None or current_fitness < best_fitness_overall:
#                 self.situational_knowledge = best_in_gen[:] # استخدام Slicing للنسخ السريع
#                 best_fitness_overall = current_fitness

#             steps_history.append((best_in_gen[:], current_fitness))

#             if current_fitness < 1000:
#                 break

#             new_population = [best_in_gen[:]] 

#             top_half = population[:max(1, self.population_size // 2)]

#             while len(new_population) < self.population_size:
#                 parent1 = random.choice(top_half)
#                 parent2 = random.choice(top_half)
#                 child = self.crossover(parent1, parent2)
#                 child = self.mutate(child)
#                 new_population.append(child)

#             population = new_population

#         exec_time = time.perf_counter() - start_time
        
#         final_conflicts = 0
#         if self.situational_knowledge:
#              final_conflicts = self.fitness(self.situational_knowledge) // 1000

        
#         return self.situational_knowledge, final_conflicts, exec_time, steps_history
import random
import time

class CulturalAlgorithm:
    def __init__(self, graph, population_size=20, generations=50,
                 mutation_rate=0.1, max_colours=4):

        self.graph = graph
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.max_colours = max_colours
        self.n = len(graph)

        self.situational_knowledge = None
        self.normative_knowledge = {
            i: set(range(max_colours)) for i in range(self.n)
        }

    def fitness(self, individual):
        conflicts = 0
        for i in range(self.n):
            if individual[i] < 0 or individual[i] >= self.max_colours:
                conflicts += 5
                continue
            for j in range(i + 1, self.n):
                if individual[j] < 0 or individual[j] >= self.max_colours:
                    continue
                if self.graph[i][j] == 1 and individual[i] == individual[j]:
                    conflicts += 1

        used_colors = len(set(c for c in individual if 0 <= c < self.max_colours))
        # High penalty for conflicts, small penalty for number of colors
        return conflicts * 1000 + used_colors

    def create_individual(self):
        individual = []
        for i in range(self.n):
            domain = list(self.normative_knowledge[i])
            valid_domain = [c for c in domain if c < self.max_colours]
            
            if not valid_domain:
                valid_domain = list(range(self.max_colours))
            
            individual.append(random.choice(valid_domain))
        return individual

    def update_belief_space(self, best):
        self.situational_knowledge = best[:]
        for i in range(self.n):
            if 0 <= best[i] < self.max_colours:
                self.normative_knowledge[i].add(best[i])

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            i = random.randint(0, self.n - 1)
            individual[i] = random.randint(0, self.max_colours - 1)
        return individual

    def crossover(self, p1, p2):
        cut = random.randint(1, self.n - 1)
        return p1[:cut] + p2[cut:]

    def repair(self, individual):
        for i in range(self.n):
            if individual[i] >= self.max_colours or individual[i] < 0:
                individual[i] = random.randint(0, self.max_colours - 1)
        return individual

    def reduce_colors(self):
        self.max_colours -= 1
        for i in range(self.n):
            self.normative_knowledge[i] = {
                c for c in self.normative_knowledge[i] if c < self.max_colours
            }
        
        if self.situational_knowledge:
            self.situational_knowledge = self.repair(self.situational_knowledge[:])

    def evolve(self):
        start = time.perf_counter()
        population = [self.create_individual() for _ in range(self.population_size)]
        steps = []
        
        # Variable to store the best VALID solution found (0 conflicts)
        best_valid_solution = None
        
        # Loop mainly controls the effort, logic inside handles color reduction
        for gen in range(self.generations):
            population.sort(key=self.fitness)
            best = population[0]
            fit = self.fitness(best)

            steps.append((best[:], fit))
            self.update_belief_space(best)
            
            # Check if current best is a valid solution (0 conflicts)
            if fit < 1000:
                # Save this solution as a backup because it's valid
                best_valid_solution = best[:]
                
                # If we have more than 1 color, try to optimize further by reducing colors
                if self.max_colours > 1:
                    self.reduce_colors()
                    # Re-initialize population to explore the new constrained space
                    population = [self.create_individual() for _ in range(self.population_size)]
                    continue # Skip to next generation with new color settings
            
            # Standard Genetic Algorithm Operations
            new_pop = [best[:]] # Elitism: keep the best
            top = population[:max(1, self.population_size // 2)]

            while len(new_pop) < self.population_size:
                p1, p2 = random.sample(top, 2)
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                child = self.repair(child)
                new_pop.append(child)

            population = new_pop

        exec_time = time.perf_counter() - start
        
        # Final Decision Logic
        current_best = population[0]
        current_conflicts = self.fitness(current_best) // 1000
        
        if current_conflicts == 0:
            # If the current state is valid (e.g., successfully reduced to 2 colors), return it
            return current_best, 0, exec_time, steps
        elif best_valid_solution is not None:
            # If current state failed (e.g., 2 colors caused conflicts), 
            # BUT we had a previous valid solution (e.g., 3 colors), REVERT to that.
            return best_valid_solution, 0, exec_time, steps
        else:
            # If we never found any valid solution, return the best effort
            return current_best, current_conflicts, exec_time, steps