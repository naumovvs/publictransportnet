from transportnet import net
from transportnet import line
from transportnet import vehicle
from stochastic import stochastic
from genetics import ga
import pandas as pd


sim_time = 4.0 * 60
model_runs = 100

n = net.Net()
# define the network configuration
n.load_from_file('verkhnodniprovsk_net.txt')
# define demand intensity
for nd in n.nodes:
    nd.s_interval = stochastic.Stochastic(law=2, scale=15)
central = n.get_node(code=1)
central.s_interval = stochastic.Stochastic(law=2, scale=5)
# define a set of public transport lines
line1 = line.Line(n, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                    13, 12, 11, 15, 16, 17, 18, 19, 1], 
                    [1, 14])
line1.add_vehicles([vehicle.Vehicle(18)])

line2 = line.Line(n, [1, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 18, 31, 32, 16, 18, 1],
                    [1, 1])
line2.add_vehicles([vehicle.Vehicle(50)])
line3 = line.Line(n, [1, 20, 33, 34, 35, 36, 37, 38,
                    37, 39, 36, 35, 18, 19, 1],
                    [1, 38])
line3.add_vehicles([vehicle.Vehicle(18)])
line4 = line.Line(n, [1, 3, 18, 40, 41, 42, 43, 44,
                    43, 42, 41, 40, 18, 3, 1],
                    [1, 44])
line4.add_vehicles([vehicle.Vehicle(38)])
line5 = line.Line(n, [1, 3, 18, 40, 41, 42, 45, 46, 47,
                    46, 45, 42, 41, 40, 18, 3, 1],
                    [1, 47])
line5.add_vehicles([vehicle.Vehicle(38)])
n.lines.extend([line1, line2, line3, line4, line5])

data = pd.read_csv('verkhnodniprovsk-best.csv', delimiter='\t', header=None)
schedules = []
for d in range(10):
    schedules.append([data[1][d], data[2][d], data[3][d], data[4][d], data[5][d]])
schedules = [[75, 90, 30, 95, 0]]

def fitness_function(shifts):
    n.reset()
    for idx in range(len(n.lines)):
        n.lines[idx].schedule_shift = shifts[idx]
    return n.simulate(sim_time)

for schedule in schedules:
    print(schedule)
    res_file = open('./verkhnodniprovsk/' + str(schedule) + '+B.txt', 'w')
    for _ in range(model_runs):
        res_str = ''
        for res in fitness_function(schedule):
            res_str += str(res) + '\t'
        res_str = res_str[:-1]
        res_file.write(res_str + '\n')
        print(res_str)
    print()
    res_file.close()