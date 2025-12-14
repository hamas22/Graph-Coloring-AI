

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

        # ---- Belief Space ----
        self.situational_knowledge = None   # best solution
        self.normative_knowledge = {
            i: set(range(max_colours)) for i in range(self.n)
        }

    # ---------------- Fitness ----------------
    def fitness(self, individual):
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.graph[i][j] == 1 and individual[i] == individual[j]:
                    conflicts += 1

        used_colors = len(set(individual))
        return conflicts * 1000 + used_colors

    # ---------------- Create Individual (Belief-guided) ----------------
    def create_individual(self):
        individual = []
        for i in range(self.n):
            domain = self.normative_knowledge[i]
            individual.append(random.choice(list(domain)))
        return individual

    # ---------------- Update Belief Space ----------------
    def update_belief_space(self, best_individual):
        self.situational_knowledge = best_individual[:]

        for i in range(self.n):
            self.normative_knowledge[i].add(best_individual[i])

    # ---------------- Genetic Ops ----------------
    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            idx = random.randint(0, self.n - 1)
            individual[idx] = random.randint(0, self.max_colours - 1)
        return individual

    def crossover(self, p1, p2):
        point = random.randint(1, self.n - 1)
        return p1[:point] + p2[point:]

    # ---------------- Reduce Colors ----------------
    def reduce_colors(self):
        self.max_colours -= 1
        for i in range(self.n):
            self.normative_knowledge[i] = {
                c for c in self.normative_knowledge[i]
                if c < self.max_colours
            }

    # ---------------- Evolution ----------------
    def evolve(self):
        start = time.perf_counter()
        population = [self.create_individual() for _ in range(self.population_size)]
        steps = []

        best_fitness = float('inf')

        for gen in range(self.generations):
            population.sort(key=self.fitness)
            best = population[0]
            fit = self.fitness(best)

            steps.append((best[:], fit))

            if fit < best_fitness:
                best_fitness = fit
                self.update_belief_space(best)

            if fit < 1000 and self.max_colours > 1:
                self.reduce_colors()
                population = [self.create_individual() for _ in range(self.population_size)]
                continue

            new_pop = [best[:]]
            top = population[:max(1, self.population_size // 2)]

            while len(new_pop) < self.population_size:
                p1, p2 = random.sample(top, 2)
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                new_pop.append(child)

            population = new_pop

        exec_time = time.perf_counter() - start
        final_conflicts = self.fitness(self.situational_knowledge) // 1000

        return self.situational_knowledge, final_conflicts, exec_time, steps
