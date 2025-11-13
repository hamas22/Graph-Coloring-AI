import random
import time

class CulturalAlgorithm:
    def __init__(self, graph, population_size=50, generations=100, mutation_rate=0.1, max_colours=4):
        self.graph = graph
        self.n = len(graph)

        #  حماس جضت يا رب نفهمه :(

        # عدد الأفراد في كل جيل 
        # if 10 or 20 Excution fast & Solve weak
        # if 100 or 200 solve vareity & long time
        # لو الجراف كبير نستخدم رقم كبير 
        self.population_size = population_size  


        # حماس جضت كمان مرة

        # عدد الأجيال 
        # if small --> fast but stop before get the best solution
        # if big --> maybe get the best solution but long time
        self.generations = generations


        # نسبة التغير العشوائي 
        # if 0.01 the evolve weak 
        # if 0.1 good balance 
        # if 0.5 many variety <-- algo is random & not learn good
        self.mutation_rate = mutation_rate
        self.max_colours = max_colours

    def fitness(self, individual):
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.graph[i][j] == 1 and individual[i] == individual[j]:
                    conflicts += 1
        return conflicts

    def initialize_population(self):
        return [[random.randint(0, self.max_colours - 1) for _ in range(self.n)] for _ in range(self.population_size)]

    def mutate(self, individual):
        idx = random.randint(0, self.n - 1)
        individual[idx] = random.randint(0, self.max_colours - 1)
        return individual

    def crossover(self, parent1, parent2):
        point = random.randint(1, self.n - 1)
        child = parent1[:point] + parent2[point:]
        return child

    def evolve(self):
        population = self.initialize_population()
        best_solution = None
        best_fitness = float('inf')
        start_time = time.time()

        for _ in range(self.generations):
            population.sort(key=self.fitness)
            if self.fitness(population[0]) < best_fitness:
                best_fitness = self.fitness(population[0])
                best_solution = population[0]

            next_gen = population[:int(0.2 * self.population_size)]
            while len(next_gen) < self.population_size:
                parent1 = random.choice(population[:10])
                parent2 = random.choice(population[:10])
                child = self.crossover(parent1, parent2)
                if random.random() < self.mutation_rate:
                    child = self.mutate(child)
                next_gen.append(child)
            population = next_gen

        end_time = time.time()
        return best_solution, best_fitness, end_time - start_time
