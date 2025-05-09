import sys
sys.path.append(".")

from transportnet import net
from transportnet import line
from transportnet import vehicle
from stochastic import stochastic
from genetics import ga
import threading as th
import time

nthreads = 1
model_runs = 10
sim_time = 4.0 * 60
nets = []

res_file = open('verkhnodniprovsk_test.txt', 'w')

for _ in range(nthreads):
    n = net.Net()
    # define the network configuration
    n.load_from_file('case studies/verkhnodniprovsk/verkhnodniprovsk_net.txt')
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
    line2 = line.Line(n, [1, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 18, 31, 32, 16, 10, 1],
                        [1, 1])
    line2.add_vehicles([vehicle.Vehicle(50)])
    line3 = line.Line(n, [1, 20, 33, 34, 35, 36, 37, 38,
                        37, 39, 36, 35, 18, 19, 1],
                        [1, 38])
    line3.add_vehicles([vehicle.Vehicle(18)])
    line4 = line.Line(n, [1, 3, 4, 40, 41, 42, 43, 44,
                        43, 42, 41, 40, 4, 3, 1],
                        [1, 44])
    line4.add_vehicles([vehicle.Vehicle(38)])
    line5 = line.Line(n, [1, 3, 4, 40, 41, 42, 45, 46, 47,
                        46, 45, 42, 41, 40, 4, 3, 1],
                        [1, 47])
    line5.add_vehicles([vehicle.Vehicle(38)])
    n.lines.extend([line1, line2, line3, line4, line5])
    # add to the collection of nets
    nets.append(n)

for iter in range(30):
   
    # s_mean_interval = stochastic.Stochastic(law=0, location=1, scale=4)
    # for nd in n.nodes:
    #     nd.s_interval = stochastic.Stochastic(law=2, scale=s_mean_interval.get_value())

    # generate demand for sim_time hours
    # n.gen_demand(sim_time)
    # print(len(n.demand))
    # print()

    def fitness_function(shifts):
        t_start = time.time()

        threads, res = [], []
        mutex = th.Lock()
        chunk = int(model_runs / nthreads)

        def run(N):
            n = nets[th.current_thread().ID]       
            for _ in range(N):
                n.reset()
                for idx in range(len(n.lines)):
                    n.lines[idx].schedule_shift = shifts[idx]
                r = n.simulate(sim_time)
                mutex.acquire()
                res.append(r)
                mutex.release()
            
        for idx in range(nthreads):
            t = th.Thread(target=run, args=(chunk,))
            t.ID = idx
            t.start()
            threads.append(t)
    
        for t in threads:
            t.join()
        
        # print(res)
        final = [0, 0, 0, 0]
        for r in res:
            for i in range(len(final)):
                final[i] += r[i]
        for idx in range(len(final)):
            final[idx] /= model_runs
        
        print(f'Fitness calc time: {time.time() - t_start}')        
        return tuple(final)

    print('iteration #', iter + 1)
    g = ga.GA()
    # 7 bits per a time shift value: in range between 0 and 127
    g.chromosome_size = len(n.lines), 7
    g.population_size = 30
    g.generations = 20
    g.fitness_function = fitness_function
    
    winner = g.run()
    print(winner)

    for w in winner[0]:
        res_file.write(str(w) + '\t')
    for w in winner[1]:
        res_file.write(str(w) + '\t')

    # res_str = ''
    # for res in fitness_function([5, 8, 0, 1, 0]):
    #     res_str += str(res) + '\t'
    #     res_file.write(str(res) + '\t')
    # print(res_str)
    res_file.write('\n')

res_file.close()