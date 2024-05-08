from stochastic import stochastic
from transportnet import line
from transportnet import net
from transportnet import vehicle

num_runs = 5
veh_capacity = 180
res_file = open('line2.txt', 'w')
for veh_num in range(2, 8 + 1, 1):
    for velocity in range(20, 30+2, 2):
        for stop_dur in range(10, 60 + 10, 10):  # [sec]
            wait_coef = 0
            for _ in range(num_runs):
                n = net.Net()
                # Cmentarz Rakowicki - Salwator
                n.add_link(1, 2, 0.19, True)
                n.add_link(2, 3, 0.25, True)
                n.add_link(3, 4, 0.31, True)
                n.add_link(4, 5, 0.33, True)
                n.add_link(5, 6, 0.47, True)
                n.add_link(6, 7, 0.47, True)
                n.add_link(7, 8, 0.58, True)
                n.add_link(8, 9, 0.56, True)
                n.add_link(9, 10, 0.57, True)
                n.add_link(10, 11, 0.51, True)
                n.add_link(11, 12, 0.34, True)
                n.add_link(12, 13, 0.24, True)

                # Salwator - Cmentarz Rakowicki
                n.add_link(2, 1, 0.21, True)
                n.add_link(3, 2, 0.25, True)
                n.add_link(4, 3, 0.37, True)
                n.add_link(5, 4, 0.32, True)
                n.add_link(6, 5, 0.48, True)
                n.add_link(7, 6, 0.46, True)
                n.add_link(8, 7, 0.61, True)
                n.add_link(9, 8, 0.53, True)
                n.add_link(10, 9, 0.6, True)
                n.add_link(11, 10, 0.41, True)
                n.add_link(12, 11, 0.52, True)
                n.add_link(13, 12, 0.1, True)

                # name the stops
                n.get_node(1).name = "Cmentarz Rakowicki"
                n.get_node(2).name = "Cmentarz Rakowicki - 2"
                n.get_node(3).name = "Rakowicka"
                n.get_node(4).name = "Uniwersytet Ekonomiczny"
                n.get_node(5).name = "Lubicz"
                n.get_node(6).name = "Teatr Slowackiego"
                n.get_node(7).name = "Stary Kleparz"
                n.get_node(8).name = "Teatr Bagatela"
                n.get_node(9).name = "Filharmonia"
                n.get_node(10).name = "Jubilat"
                n.get_node(11).name = "Komorowskiego"
                n.get_node(12).name = "Salwator"
                n.get_node(13).name = "Salwator"

                # set matrices of passengers' arrival and depature at the bus stops
                f_direct_in = open('cmentarz-salwator-in.txt')
                lns_direct_in = f_direct_in.readlines()
                f_direct_in.close()
                f_back_in = open('salwator-cmentarz-in.txt')
                lns_back_in = f_back_in.readlines()
                f_back_in.close()
                f_direct_out = open('cmentarz-salwator-out.txt')
                lns_direct_out = f_direct_out.readlines()
                f_direct_out.close()
                f_back_out = open('salwator-cmentarz-out.txt')
                lns_back_out = f_back_out.readlines()
                f_back_out.close()
                # print(lns_direct_in)
                # matrix of passengers' departure from the bus stops in main direction
                ps_direct_in = []
                for ln in lns_direct_in:
                    ps_direct_in.append([int(el) for el in ln.split('\t')])
                # print(ps_direct_in)
                # matrix of passengers' departure from the bus stops in back direction
                ps_back_in = []
                for ln in lns_back_in:
                    ps_back_in.append([int(el) for el in ln.split('\t')])
                # matrix of passengers' arrivals in main direction
                ps_direct_out = []
                for ln in lns_direct_out:
                    ps_direct_out.append([int(el) for el in ln.split('\t')])
                # matrix of passengers' arrivals in back direction
                ps_back_out = []
                for ln in lns_back_out:
                    ps_back_out.append([int(el) for el in ln.split('\t')])


                # simulate the average demand interval for the nodes
                for node in n.nodes:
                    node.s_interval = stochastic.Stochastic(law=2,
                                                            scale=stochastic.Stochastic(law=1,
                                                                                        location=2,
                                                                                        scale=0.5).get_value())
                # set a trace of the line #2
                line2 = line.Line(n, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
                # add vehicles operating at the line #2
                line2.add_vehicles([vehicle.Vehicle(veh_capacity) for __ in range(veh_num)])
                line2.velocity = velocity
                line2.intermediate_stop_duration = 1.0*stop_dur/60  # [min]
                # add tne line #129 to the net
                n.lines.append(line2)
                # simulate the line operation
                n.simulate(duration=4*60)
                # print out characteristics of the net
                # n.print_characteristics()
                # n.print_od_matrix()
                wait_coef += 1.0 * n.total_wait_time / n.duration
            print(veh_num, velocity, stop_dur, wait_coef / num_runs)
            res_file.write(str(veh_num) + '\t' + str(velocity) + '\t' +
                           str(stop_dur) + '\t' + str(wait_coef / num_runs) + '\n')
res_file.close()