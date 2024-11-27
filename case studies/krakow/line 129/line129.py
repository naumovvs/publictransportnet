import sys
sys.path.append(".")

from stochastic import stochastic
from transportnet import line
from transportnet import net
from transportnet import vehicle

num_runs = 5
veh_capacity = 42 + 98
for veh_num in range(5, 10 + 1, 1):
    for velocity in range(20, 40+2, 2):
        for stop_dur in range(30, 180 + 30, 30):  # [sec]
            wait_coef = 0
            for _ in range(num_runs):
                n = net.Net()
                # Dworec Glowny Zachod - Czyzyny Dworzec
                n.add_link(1, 2, 0.4, True)
                n.add_link(2, 3, 0.6, True)
                n.add_link(3, 4, 0.23, True)
                n.add_link(4, 5, 0.55, True)
                n.add_link(5, 6, 0.7, True)
                n.add_link(6, 7, 0.45, True)
                n.add_link(7, 8, 0.65, True)
                n.add_link(8, 9, 0.55, True)
                n.add_link(9, 10, 0.24, True)
                n.add_link(10, 11, 0.8, True)
                n.add_link(11, 12, 0.55, True)
                n.add_link(12, 13, 0.6, True)
                n.add_link(13, 14, 0.45, True)
                n.add_link(14, 15, 0.5, True)
                n.add_link(15, 16, 0.35, True)
                n.add_link(16, 17, 1.4, True)
                n.add_link(17, 18, 0.55, True)
                n.add_link(18, 19, 0.6, True)
                # Czyzyny Dworzec - Dworec Glowny Zachod
                n.add_link(2, 1, 0.6, True)
                n.add_link(3, 2, 0.8, True)
                n.add_link(4, 3, 0.3, True)
                n.add_link(5, 4, 0.5, True)
                n.add_link(6, 5, 0.25, True)
                n.add_link(7, 6, 0.65, True)
                n.add_link(8, 7, 0.45, True)
                n.add_link(9, 8, 0.35, True)
                n.add_link(10, 9, 0.65, True)
                n.add_link(11, 10, 0.35, True)
                n.add_link(12, 11, 0.4, True)
                n.add_link(13, 12, 0.4, True)
                n.add_link(14, 13, 0.5, True)
                n.add_link(15, 14, 0.45, True)
                n.add_link(16, 15, 0.4, True)
                n.add_link(17, 16, 1.1, True)
                n.add_link(18, 17, 0.27, True)
                n.add_link(19, 18, 0.65, True)
                # name the stops
                n.get_node(1).name = "Dworzec Glowny Zachod"
                n.get_node(2).name = "Politechnika"
                n.get_node(3).name = "Cmentarz Rakowicki"
                n.get_node(4).name = "Biskupa Prandoty"
                n.get_node(5).name = "Uniwersytet Rolniczy"
                n.get_node(6).name = "Brogi"
                n.get_node(7).name = "Bosakow"
                n.get_node(8).name = "Miechowity"
                n.get_node(9).name = "Rondo Mlynskie"
                n.get_node(10).name = "Miechowity 2"
                n.get_node(11).name = "Rondo Barei"
                n.get_node(12).name = "Park Wodny"
                n.get_node(13).name = "Os. Oswiecenia"
                n.get_node(14).name = "Okulickiego"
                n.get_node(15).name = "Wislicka"
                n.get_node(16).name = "Os. Dywizjonu 303"
                n.get_node(17).name = "Stella-Sawickiego"
                n.get_node(18).name = "Medweckiego"
                n.get_node(19).name = "Czyzyny Dworzec"
                # simulate the average demand interval for the nodes
                for node in n.nodes:
                    node.s_interval = stochastic.Stochastic(law=2,
                                                            scale=stochastic.Stochastic(law=1,
                                                                                        location=2,
                                                                                        scale=0.5).get_value())
                # set a trace of the line #129
                line129 = line.Line(n, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
                # add vehicles operating at the line #129
                line129.add_vehicles([vehicle.Vehicle(veh_capacity) for __ in range(veh_num)])
                line129.velocity = velocity
                line129.intermediate_stop_duration = 1.0*stop_dur/60  # [min]
                # add tne line #129 to the net
                n.lines.append(line129)
                # simulate the line operation
                n.simulate(duration=18*60)
                # print out characteristics of the net
                # n.print_characteristics()
                # n.print_od_matrix()
                wait_coef += 1.0 * n.total_wait_time / n.duration
            print(veh_num, velocity, stop_dur, wait_coef / num_runs)
