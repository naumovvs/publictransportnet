from transportnet import line
from transportnet import net
from transportnet import vehicle

#import matplotlib.pyplot as plt


n = net.Net()
# Struga - Chelmonskiego Osiedle
n.add_link(1, 2, 0.73, True)
n.add_link(2, 3, 0.43, True)
n.add_link(3, 4, 0.41, True)
n.add_link(4, 5, 0.44, True)
n.add_link(5, 6, 0.94, True)
n.add_link(6, 7, 1.23, True)
n.add_link(7, 8, 0.92, True)
n.add_link(8, 9, 1.59, True)
n.add_link(9, 10, 0.78, True)
n.add_link(10, 11, 2.35, True)
n.add_link(11, 12, 0.46, True)
n.add_link(12, 13, 0.69, True)
n.add_link(13, 14, 1.01, True)
n.add_link(14, 15, 0.89, True)
n.add_link(15, 16, 0.48, True)
n.add_link(16, 17, 1.27, True)
n.add_link(17, 18, 0.58, True)
n.add_link(18, 19, 1.23, True)
n.add_link(19, 20, 0.41, True)
n.add_link(20, 21, 0.85, True)
n.add_link(21, 22, 1.30, True)
# Chelmonskiego Osiedle - Struga
n.add_link(3, 1, 0.96, True)
n.add_link(4, 3, 0.62, True)
n.add_link(5, 4, 0.35, True)
n.add_link(6, 5, 0.92, True)
n.add_link(7, 6, 1.32, True)
n.add_link(8, 7, 0.88, True)
n.add_link(9, 8, 1.55, True)
n.add_link(10, 9, 0.87, True)
n.add_link(11, 10, 2.17, True)
n.add_link(12, 11, 0.89, True)
n.add_link(13, 12, 0.81, True)
n.add_link(14, 13, 0.71, True)
n.add_link(15, 14, 0.92, True)
n.add_link(16, 15, 0.57, True)
n.add_link(17, 16, 1.26, True)
n.add_link(18, 17, 0.54, True)
n.add_link(19, 18, 1.30, True)
n.add_link(20, 19, 0.55, True)
n.add_link(21, 20, 0.58, True)
n.add_link(23, 21, 0.80, True)
n.add_link(22, 23, 0.55, True)
# name the stops
n.get_node(1).name = "Struga"
n.get_node(2).name = "Aleja Roz"
n.get_node(3).name = "Zeromskiego"
n.get_node(4).name = "Teatr Ludowy"
n.get_node(5).name = "Arka"
n.get_node(6).name = "Rondo Hipokratesa"
n.get_node(7).name = "Os.Na Lotnisku"
n.get_node(8).name = "Wislicka"
n.get_node(9).name = "Bora-Komorowskiego"
n.get_node(10).name = "Miechowity"
n.get_node(11).name = "Rondo Mogilskie"
n.get_node(12).name = "Uniwersytet Ekonomiczny"
n.get_node(13).name = "Politechnika"
n.get_node(14).name = "Nowy Kleparz"
n.get_node(15).name = "Plac Inwalidow"
n.get_node(16).name = "Czarnowiejska"
n.get_node(17).name = "Miasteczko Studenckie AGH"
n.get_node(18).name = "Przybyszewskiego"
n.get_node(19).name = "Zarzecze"
n.get_node(20).name = "Bronowice Wiadukt"
n.get_node(21).name = "Rondo Ofiar Katynia"
n.get_node(22).name = "Chelmonskiego Osiedle"
n.get_node(23).name = "Stawowa"
# set matrices of passengers' arrival and depature at the bus stops
f_direct_in = file('s-ch_in.txt')
lns_direct_in = f_direct_in.readlines()
f_direct_in.close()
f_back_in = file('ch-s_in.txt')
lns_back_in = f_back_in.readlines()
f_back_in.close()
f_direct_out = file('s-ch_out.txt')
lns_direct_out = f_direct_out.readlines()
f_direct_out.close()
f_back_out = file('ch-s_out.txt')
lns_back_out = f_back_out.readlines()
f_back_out.close()
# matrix of passengers' departure from the bus stops in main direction
ps_direct_in = []
for ln in lns_direct_in:
    ps_direct_in.append([int(el) for el in ln.split('\t')])
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
# set parameters of the line #501
veh_capacity = 42 + 98
# simulate the line operation
for veh_num in range(1, 2, 1):
    for exp_num in range(30):
        # set demand parameters
        for nd in n.nodes:
            nd.direct_in = ps_direct_in[nd.code - 1]
            nd.direct_out = ps_direct_out[nd.code - 1]
            nd.back_in = ps_back_in[nd.code - 1]
            nd.back_out = ps_back_out[nd.code - 1]
            nd.pass_in = []
            nd.pass_out = []
        # add tne line #501 to the net
        line501 = line.Line(n, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                23, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 1])
        line501.velocity = 45
        line501.intermediate_stop_duration = 1.0 * 45 / 60  # [min]
        line501.add_vehicles([vehicle.Vehicle(veh_capacity) for _ in range(veh_num)])
        n.lines = []
        n.total_wait_time = 0
        n.sum_vehicles_time = 0
        n.num_serviced_passengers = 0
        # add tne line #501 to the net
        n.lines.append(line501)
        n.simulate(duration=18*60)
        print veh_num, n.total_wait_time
#n.gen_demand(duration=18*60, is_stochastic=False)
# for nd in n.nodes:
#     print nd.direct_out, nd.back_out
# print out characteristics of the net
#n.print_characteristics()
#n.print_od_matrix()
