from genetics.chromosome import Chromosome
import random


class Population:
    """
    population of chromosomes
    """

    def __init__(self):
        self.size = 50
        self.chromosome_size = (8, 8)
        #
        self.fitness_function = None
        self.maximize = False
        #
        self.survivors_rate = 0.1
        self.crossover_probability = 0.25
        self.mutation_probability = 0.05
        self.mutation_turns = 1
        #
        self.chromosomes = []

    def initiate(self):
        self.chromosomes = [Chromosome(self.chromosome_size, None)
                            for _ in range(self.size)]

    def evolve(self, generations=100):
        winner = (None, 0)
        survivors_number = int(round(self.size * self.survivors_rate))
        for g in range(generations):
            # evaluation
            estimates = [(c.evaluate(self.fitness_function), c)
                         for c in self.chromosomes]
            # ranking selection
            estimates.sort(key=lambda e: e[0][0], reverse=self.maximize)
            ranked_items = [item[1] for item in estimates]
            survivors = ranked_items[:survivors_number]
            # print out the winner
            winner = survivors[0].decode(), estimates[0][0]
            print("winner", g + 1, winner[0], winner[1])
            # reproduction
            self.chromosomes = survivors # []
            while len(self.chromosomes) < self.size:
                parent1 = survivors[random.randint(0, survivors_number - 1)]
                parent2 = survivors[random.randint(0, survivors_number - 1)]
                # crossover
                offspring = parent1.replicate(parent2, self.crossover_probability)
                # mutation
                offspring.mutate(self.mutation_probability, self.mutation_turns)
                self.chromosomes.append(offspring)
        return winner

    def printout(self):
        for c in self.chromosomes:
            print(c.genes, c.decode())

