
import random
import copy

class CulturalAlgorithm:
    def __init__(self, graph, population_size=20, generations=50, mutation_rate=0.1, max_colours=4):
        self.graph = graph


         # عدد الأفراد في كل جيل 
         # if 10 or 20 Excution fast & Solve weak
         # if 100 or 200 solve vareity & long time
         # لو الجراف كبير نستخدم رقم كبير 
        self.population_size = population_size


         # عدد الأجيال 
         # if small --> fast but stop before get the best solution
         # if big --> maybe get the best solution but long time
        self.generations = generations


        # if 0.01 the evolve weak 
        # if 0.1 good balance 
        # if 0.5 many variety <-- algo is random & not learn good
        self.mutation_rate = mutation_rate
        self.max_colours = max_colours
        self.n = len(graph)
        self.situational_knowledge = None 
        self.normative_knowledge = {} 

    def fitness(self, individual):
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.graph[i][j] == 1 and individual[i] == individual[j]:
                    conflicts += 1
        return conflicts

    def create_individual(self):
        return [random.randint(0, self.max_colours - 1) for _ in range(self.n)]

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            idx = random.randint(0, self.n - 1)
            individual[idx] = random.randint(0, self.max_colours - 1)
        return individual

    def crossover(self, p1, p2):
        point = random.randint(1, self.n - 1)
        child = p1[:point] + p2[point:]
        return child

    def evolve(self):
        import time
        start_time = time.time()
        
# Random colors
        population = [self.create_individual() for _ in range(self.population_size)]
        
# storage the evolve
        steps_history = [] 

        for generation in range(self.generations):

            population.sort(key=self.fitness)
            best_in_gen = population[0]
            best_fitness = self.fitness(best_in_gen)

            if self.situational_knowledge is None or best_fitness < self.fitness(self.situational_knowledge):
                self.situational_knowledge = copy.deepcopy(best_in_gen)

            steps_history.append((copy.deepcopy(best_in_gen), best_fitness))

            if best_fitness == 0:
                break

            new_population = [best_in_gen] 
            
            while len(new_population) < self.population_size:
                parent1 = random.choice(population[:self.population_size//2]) # Select from top 50%
                parent2 = random.choice(population[:self.population_size//2])
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            
            population = new_population

        exec_time = time.time() - start_time
        
        return self.situational_knowledge, self.fitness(self.situational_knowledge), exec_time, steps_history