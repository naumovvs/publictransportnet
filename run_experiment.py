from stochastic import stochastic
from transportnet import line, vehicle
from transportnet import net

res_file = open("res_full_wait.txt", 'w')

mean_in_series = []
var_in_series = []
need_observation_in_series = []
series_input = []

# network simulation experiment
for veh_number in range(1, 9+2, 2):
    for mean_int in range(1, 9+2, 2):
        for stops_number in range(2, 10+2, 2):
            for mean_dist in range(1, 3+1, 1):
                for capacity in range(10, 70+30, 30):
                    # runs of the experiment
                    twt = []
                    mean_twt = 0
                    for runs in range(100):
                        # forming the network
                        n = net.Net()
                        for i in range(2, stops_number+1):
                            n.add_link(i - 1, i,
                                       stochastic.Stochastic(law=1,
                                                             location=mean_dist,
                                                             scale=0.2*mean_dist
                                                             ).get_value()
                                       )
                        # define the route path
                        l = line.Line(n, range(1, stops_number+1))
                        # defining the route fleet
                        # vehicles = []
                        # for i in range(veh_number):
                        #     vehicles.append(vehicle.Vehicle(capacity))
                        l.add_vehicles([vehicle.Vehicle(capacity) for _ in range(veh_number)])
                        # add the line to the network
                        n.lines.append(l)
                        # generating the mean intervals for passengers arrivals to the network (line) nodes
                        for node in n.nodes:
                            node.s_interval = stochastic.Stochastic(law=2,
                                                                    scale=stochastic.Stochastic(law=1,
                                                                                                location=mean_int,
                                                                                                scale=0.2*mean_int).
                                                                    get_value()
                                                                    )
                        # simulation run
                        n.simulate()
                        mean_twt += n.total_wait_time
                        twt.append(n.total_wait_time)
                        print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t"\
                            .format(veh_number, mean_int, stops_number, mean_dist, capacity, n.total_wait_time))
                        res_file.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n"
                                       .format(veh_number, mean_int, stops_number, mean_dist, capacity,
                                               n.total_wait_time)
                                       )
                    mean_twt /= len(twt)# - 1
                    var_twt = 0
                    for t in twt:
                        var_twt += (mean_twt - t) * (mean_twt - t)
                    var_twt /= len(twt) - 1
                    series_input.append([veh_number, mean_int, stops_number, mean_dist, capacity])
                    mean_in_series.append(mean_twt)
                    var_in_series.append(var_twt)
                    t_alfa = 1.984217
                    need_observation_in_series.append(round(t_alfa*t_alfa*var_twt/(0.05*0.05*mean_twt*mean_twt), 0))

res_file.write("\n Experiment statistics:\n")
max_var = var_in_series[0]
sum_var = 0
for i in range(len(series_input)):
    sum_var += var_in_series[i]
    if var_in_series[i] > max_var:
        max_var = var_in_series[i]
    res_file.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(i, series_input[i], mean_in_series[i], var_in_series[i],
                                                      need_observation_in_series[i]))
res_file.write("Cochran-test value: {0}".format(round(max_var / sum_var, 4)))
res_file.close()

''''
print
print str(n.lines[0].line_end_stops[0].code) + " to " + str(n.lines[0].line_end_stops[-1].code)
print n.lines[0].turnaround_time, line1.turns_number
nds = n.lines[0].nodes_sequence
print "nds length =", len(nds)
for idx in range(0, len(nds)):
#for nds in line1.get_nodes_sequence(line1.turns_number):
    print nds[idx].code,
print
print
'''

'''
# not-serviced passengers

for nd in n.nodes:
    print "-------------------------------------------"
    print "node " + str(nd.code) + " demand interval is " + str(nd.s_interval.scale) + " min."
    pn = 0
    for psgr in nd.pass_out:
        pn += 1
        print "psgr #" + str(pn) + " app. time is " + str(psgr.m_appearance) + " min., from " + \
              str(psgr.origin_node.code) + " to " + str(psgr.destination_node.code)


for v in n.lines[0].vehicles:
    for s in v.schedule:
        print s[0], s[1].code,
        for pas in v.servicing[s]:
            print str(pas.origin_node.code) + "-" + str(pas.destination_node.code) + " : ",
        print
    print
'''
#app.MainLoop()

