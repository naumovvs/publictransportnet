import sys
sys.path.append(".")

from transfernode import node
from transfernode import line
from stochastic import stochastic
from genetics import ga


avtovokzal = node.Node()
# start times counting from 5AM: [75, 90, 30, 95, 0]
# start times counting from 6:30AM: [20, 0, 0, 5, 14]
line1 = line.Line(20, 15+20, stochastic.Stochastic(1, 3, 0.5), 0.35, "#1")
line2 = line.Line(0, 30, stochastic.Stochastic(1, 4, 1), 0.20, "#2")
line3 = line.Line(0, 20, stochastic.Stochastic(1, 5, 1), 0.25, "#3")
line4 = line.Line(5, 28, stochastic.Stochastic(1, 4, 0.5), 0.10, "#4")
line5 = line.Line(14, 26, stochastic.Stochastic(1, 4, 0.5), 0.10, "#5")

avtovokzal.origin_pass_number = 250  # [pas./h]
avtovokzal.lines = [line1, line2, line3, line4, line5]

nd, dur, N = avtovokzal, 180, 30

def fitness_function(shifts):
    for idx in range(len(nd.lines)):
        nd.lines[idx].shift = shifts[idx]
    res = 0.0
    for _ in range(N):
        res += nd.simulate(duration=dur)
    return res / N

g = ga.GA()
# 7 bits per a time shift value: in range between 0 and 127
g.chromosome_size = len(avtovokzal.lines), 7
g.population_size = 100
g.generations = 30
g.fitness_function = fitness_function
winner = g.run()
print (fitness_function(winner[0]))

# f = open('avtovokzal_results.csv', 'w')
# for _ in range(300):
#     f.write(f'{fitness_function([22, 17, 9, 18, 11])}\t{fitness_function([20, 0, 0, 5, 14])}\n')
# f.close()

# print (fitness_function([21, 19, 8, 22, 12]))
# # from 5:00
# print (fitness_function([75, 90, 30, 95, 0]))
# # from 5:52
# print (fitness_function([75-52, 90-52, 30-52+20+20, 95-52, 0-52+26+26]))
# from 6:30: [20, 0, 0, 5, 14]
# print (fitness_function([75-90+35, 90-90, 30-90+20+20+20, 95-90, 0-90+26+26+26+26]))

