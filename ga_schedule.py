from transportnet import net
from transportnet import line
from transportnet import vehicle
from stochastic import stochastic
from genetics import ga


sim_time = 1.0 * 60
res_file = open('results.txt', 'w')
for sn in range(30):
    n = net.Net()
    # define the network configuration
    n.load_from_file('bochnia_net.txt')
    # conf #1
    # n.add_link(1, 2, 1.0)
    # n.add_link(3, 2, 2.0)
    # n.add_link(2, 4, 2.0)
    # n.add_link(5, 4, 3.0)
    # n.add_link(4, 6, 1.0)
    # n.add_link(2, 7, 1.0)
    # n.add_link(4, 8, 2.0)
    # n.add_link(9, 7, 1.0)
    # n.add_link(7, 8, 3.0)
    # n.add_link(8, 10, 2.0)
    # n.add_link(7, 11, 3.0)
    # n.add_link(8, 12, 2.0)
    #
    # conf #2
    # s_weight = stochastic.Stochastic(0, 0.9, 1.1)
    # n.add_link(1, 3, s_weight.get_value())
    # n.add_link(3, 4, s_weight.get_value())
    # n.add_link(2, 4, s_weight.get_value())
    # n.add_link(4, 5, s_weight.get_value())
    # n.add_link(4, 6, s_weight.get_value())
    # n.add_link(5, 8, s_weight.get_value())
    # n.add_link(6, 9, s_weight.get_value())
    # n.add_link(7, 8, s_weight.get_value())
    # n.add_link(8, 9, s_weight.get_value())
    # n.add_link(9, 10, s_weight.get_value())
    # n.add_link(8, 11, s_weight.get_value())
    # n.add_link(9, 12, s_weight.get_value())
    # n.add_link(11, 13, s_weight.get_value())
    # n.add_link(12, 14, s_weight.get_value())
    #
    # conf #3
    # n.add_link(1, 2, s_weight.get_value())
    # n.add_link(2, 3, s_weight.get_value())
    # n.add_link(3, 4, s_weight.get_value())
    # n.add_link(4, 5, s_weight.get_value())
    # n.add_link(5, 6, s_weight.get_value())
    # n.add_link(6, 7, s_weight.get_value())
    # n.add_link(8, 3, s_weight.get_value())
    # n.add_link(3, 9, s_weight.get_value())
    # n.add_link(9, 10, s_weight.get_value())
    # n.add_link(10, 11, s_weight.get_value())
    # n.add_link(11, 12, s_weight.get_value())
    # n.add_link(13, 14, s_weight.get_value())
    # n.add_link(14, 10, s_weight.get_value())
    # n.add_link(10, 15, s_weight.get_value())
    # n.add_link(15, 16, s_weight.get_value())
    # n.add_link(16, 17, s_weight.get_value())
    # n.add_link(17, 18, s_weight.get_value())
    # n.add_link(18, 19, s_weight.get_value())
    # n.add_link(20, 21, s_weight.get_value())
    # n.add_link(21, 10, s_weight.get_value())
    # n.add_link(10, 22, s_weight.get_value())
    # n.add_link(22, 23, s_weight.get_value())
    # n.add_link(23, 5, s_weight.get_value())
    # n.add_link(5, 24, s_weight.get_value())
    # n.add_link(25, 5, s_weight.get_value())
    # n.add_link(5, 26, s_weight.get_value())
    # n.add_link(26, 27, s_weight.get_value())
    # n.add_link(27, 17, s_weight.get_value())
    # n.add_link(17, 28, s_weight.get_value())
    # n.add_link(28, 29, s_weight.get_value())
    # n.add_link(29, 30, s_weight.get_value())

    s_mean_interval = stochastic.Stochastic(law=0, location=1, scale=4)
    for nd in n.nodes:
        nd.s_interval = stochastic.Stochastic(law=2, scale=s_mean_interval.get_value())

    # define a set of public transport lines
    bochnia_lines = [line.Line(n, [27, 28, 39, 18, 23, 26, 15, 31, 32,
                                   31, 15, 26, 23, 18, 35, 25, 27], [27, 32]),
                     line.Line(n, [27, 28, 39, 18, 9, 11, 7, 8, 10, 4, 5, 6,
                                   5, 4, 10, 8, 7, 11, 9, 18, 35, 25, 27], [27, 6]),
                     line.Line(n, [18, 35, 20, 21, 22, 19, 14, 12, 13,
                                   12, 14, 19, 22, 21, 20, 35, 18], [18, 13]),
                     line.Line(n, [27, 28, 39, 18, 23, 24, 17, 16, 40, 41, 30, 42, 43, 2, 3, 33, 34, 29,
                                   34, 1, 2, 36, 37, 38, 37, 36, 43, 42, 30, 41, 40, 16, 17, 24, 23, 18, 35, 25, 27], [27, 29])]
    # conf #2
    # lines = [line.Line(n, [1, 3, 4, 6, 9, 12, 14]),
    #          line.Line(n, [2, 4, 5, 8, 11, 13]),
    #          line.Line(n, [7, 8, 9, 10])]
    # conf #3
    # lines = [line.Line(n, [1, 2, 3, 4, 5, 6, 7]),
    #          line.Line(n, [8, 3, 9, 10, 11, 12]),
    #          line.Line(n, [13, 14, 10, 15, 16, 17, 18, 19]),
    #          line.Line(n, [20, 21, 10, 22, 23, 5, 24]),
    #          line.Line(n, [25, 5, 26, 27, 17, 28, 29, 30])]

    for ln in bochnia_lines:
        ln.add_vehicles([vehicle.Vehicle(45) for _ in range(2)])
    n.lines.extend(bochnia_lines)

    # generate demand for sim_time hours
    n.gen_demand(sim_time)
    n.print_od_matrix()
    print
    print 'population #', sn


    def fitness_function(shifts):
        n.reset()
        for idx in range(len(n.lines)):
            n.lines[idx].schedule_shift = shifts[idx]
        return n.simulate(sim_time)

    g = ga.GA()
    # 5 bits per a time shift value: in range between 0 and 31
    g.chromosome_size = len(n.lines), 5
    g.population_size = 50
    g.generations = 30
    g.fitness_function = fitness_function
    winner = g.run()
    for w in winner[0]:
        res_file.write(str(w) + '\t')
    for w in winner[1]:
        res_file.write(str(w) + '\t')
    res_file.write('\n')
    print

res_file.close()

