from transfernode import node
from transfernode import line
from stochastic import stochastic
from genetics import ga


wislicka = node.Node()
line125 = line.Line(14, 20, stochastic.Stochastic(1, 2.50, 1.02), 0.0149, "125")
line129 = line.Line(10, 15, stochastic.Stochastic(1, 3.30, 1.65), 0.0301, "129")
line132 = line.Line(13, 20, stochastic.Stochastic(1, 2.08, 1.41), 0.0302, "132")
line138 = line.Line(1, 20, stochastic.Stochastic(1, 3.47, 2.03), 0.0542, "138")
line152 = line.Line(7, 20, stochastic.Stochastic(1, 3.77, 2.00), 0.0471, "152")
line159 = line.Line(4, 15, stochastic.Stochastic(1, 8.83, 2.25), 0.0696, "159")
line172 = line.Line(1, 20, stochastic.Stochastic(1, 4.85, 1.60), 0.0836, "172")
line192 = line.Line(19, 20, stochastic.Stochastic(1, 3.43, 1.45), 0.0282, "192")
line429 = line.Line(4, 15, stochastic.Stochastic(1, 1.83, 1.34), 0.0235, "429")
line501 = line.Line(12, 15, stochastic.Stochastic(1, 3.47, 1.61), 0.1442, "501")
line502 = line.Line(1, 10, stochastic.Stochastic(1, 4.75, 2.03), 0.2569, "502")
line511 = line.Line(5, 15, stochastic.Stochastic(1, 5.11, 2.05), 0.1113, "511")
line572 = line.Line(12, 20, stochastic.Stochastic(1, 2.96, 1.49), 0.1060, "572")
wislicka.origin_pass_number = 402  # [pas./h]
wislicka.lines = [line125, line129, line132, line138, line152, line159, line172,
                  line192, line429, line501, line502, line511, line572]


def fitness_function(shifts):
    for idx in range(len(wislicka.lines)):
        wislicka.lines[idx].shift = shifts[idx]
    res = 0
    for _ in range(50):
        res += wislicka.simulate()
    return res / 50

g = ga.GA()
# 5 bits per a time shift value: in range between 0 and 31
g.chromosome_size = len(wislicka.lines), 5
g.population_size = 100
g.generations = 30
g.fitness_function = fitness_function
winner = g.run()
for w in winner[0]:
    print (str(w),)
print (winner[1])

print (fitness_function([14, 10, 13, 1, 7, 4, 1, 19, 4, 12, 1, 5, 12]))
