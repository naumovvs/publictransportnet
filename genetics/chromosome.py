import random


class Chromosome:
    """ genotype representation """

    def __init__(self, size=(8, 8), code=None):
        self.size = size
        self.length = self.size[0] * self.size[1]
        if code is not None:
            self.genes = code
        else:
            self.genes = [random.randint(0, 1) for _ in range(self.length)]

    def decode(self):
        units, bits = self.size[0], self.size[1]
        xs = [0 for _ in range(units)]
        for j in range(units):
            xs[j] = sum([2 ** (bits - i - 1) * self.genes[j * bits + i]
                         for i in range(bits)])
        return xs

    def evaluate(self, fitness_function):
        return fitness_function(self.decode())

    def mutate(self, prob=0.05, turns=1):
        """ mutation """
        for item in range(turns):
            if random.random() < prob:
                gene_to_change = random.randint(0, self.length - 1)
                self.genes[gene_to_change] = (self.genes[gene_to_change] + 1) % 2

    def replicate(self, another, prob=0.25):
        """ crossover """
        code = self.genes[:]
        if random.random() < prob:
            part = random.randint(1, self.length - 2)
            code = self.genes[:part] + another.genes[part:]
        return Chromosome(self.size, code)

