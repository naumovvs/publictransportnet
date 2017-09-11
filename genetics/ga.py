from chromosome import Chromosome
from population import Population


class GA:

    def __init__(self):
        # scale parameters
        self.chromosome_size = (8, 8)
        self.population_size = 20
        self.generations = 50
        # fitness function
        self.fitness_function = None
        self.maximize = False
        # genetic parameters
        self.survivors_rate = 0.2
        self.crossover_probability = 0.5
        self.mutation_probability = 0.1
        self.mutation_turns = 3

    def run(self):
        pop = Population()
        pop.size = self.population_size
        pop.chromosome_size = self.chromosome_size
        #
        pop.fitness_function = self.fitness_function
        pop.maximize = self.maximize
        #
        pop.survivors_rate = self.survivors_rate
        pop.crossover_probability = self.crossover_probability
        pop.mutation_probability = self.mutation_probability
        pop.mutation_turns = self.mutation_turns
        #
        pop.initiate()
        return pop.evolve(self.generations)

