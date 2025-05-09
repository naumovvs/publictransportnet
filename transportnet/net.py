import random
import numpy as np
# import threading as th
from stochastic import stochastic
from transportnet import line
from transportnet import link
from transportnet import node
from transportnet import passenger


class Net:
    """
        Net as the graph model
    """

    def __init__(self):
        # network model time
        self.time = 0
        # duration of the network simulation [minutes]
        self.duration = 0
        # network geography
        self.nodes = []
        self.links = []
        self.lines = []
        # transport demand
        self.demand = []

    @property
    def total_wait_time(self):
        return sum([p.wait_time for p in self.demand])

    @property
    def sum_vehicles_time(self):
        sum_vehicles_time = 0
        for ln in self.lines:
            for v in ln.vehicles:
                sum_vehicles_time += v.schedule[-1][0] - v.schedule[0][0]
        return sum_vehicles_time

    @property
    def transfer_nodes(self):
        transfers = []
        for a_line in self.lines:
            for nd in a_line.nodes:
                for other_line in self.lines:
                    if a_line is not other_line and \
                                    nd in other_line.nodes and\
                                    nd not in transfers:
                        transfers.append(nd)
        return transfers

    def contains_node(self, node_code):
        """"
            Determines if the network contains a node with the specified code
        """
        for n in self.nodes:
            if n.code == node_code:
                return True
        return False

    def get_node(self, code):
        """"
            Returns the first found node with the specified code
        """
        for n in self.nodes:
            if n.code == code:
                return n
        return None

    def contains_link(self, out_node, in_node):
        """
            Checks if the net contains a link
        """
        for lnk in self.links:
            if lnk.out_node is out_node and lnk.in_node is in_node:
                return True
        return False

    def get_link(self, out_node, in_node):
        """" Returns the first found link with the specified out and in nodes """
        for lnk in self.links:
            if lnk.out_node is out_node and lnk.in_node is in_node:
                return lnk
        return None

    def add_link(self, out_code, in_code, weight=0, directed=False, track=[]):
        """
            Adds a link with the specified characteristics
        """
        if self.contains_node(out_code):
            # out-node is already in the net
            out_node = self.get_node(out_code)
            if self.contains_node(in_code):
                # in-node is already in the net
                in_node = self.get_node(in_code)
                if self.contains_link(out_node, in_node):
                    # out-node and in-node are already linked: change the link weight
                    lnk = self.get_link(out_node, in_node)
                    lnk.weight = weight
                    lnk.track = track
                else:
                    # there is no such a link in the net: add a new one
                    new_link = link.Link(out_node, in_node, weight)
                    new_link.track = track
                    out_node.out_links.append(new_link)
                    in_node.in_links.append(new_link)
                    self.links.append(new_link)
            else:
                # the net contains the specified out-node, but there is no in-node with the specified code
                in_node = node.Node(in_code)
                new_link = link.Link(out_node, in_node, weight)
                new_link.track = track
                out_node.out_links.append(new_link)
                in_node.in_links.append(new_link)
                self.nodes.append(in_node)
                self.links.append(new_link)
        else:
            # the net does not contain the specified out-node
            out_node = node.Node(out_code)
            if self.contains_node(in_code):
                # in-node is already in the net
                in_node = self.get_node(in_code)
            else:
                # there are no in-node and out-node with the specified codes
                in_node = node.Node(in_code)
                self.nodes.append(in_node)
            # create new link
            new_link = link.Link(out_node, in_node, weight)
            new_link.track = track
            out_node.out_links.append(new_link)
            in_node.in_links.append(new_link)
            self.nodes.append(out_node)
            self.links.append(new_link)
        # add the reverse link
        if not directed:
            self.add_link(in_code, out_code, weight, True, track[::-1])
        # sort the nodes (is useful for calculating the short distances matrix)
        # self.nodes.sort()

    def generate(self, nodes_num, links_num, s_weight):
        """
            nodes_num - number of nodes in the net
            links_num - number of links in the net
            s_weight - stochastic variable of the links weight
        """
        # limit lower bound for the number of nodes
        if nodes_num < 2:
            nodes_num = 2
        # limit lower bound for the number of links
        if links_num < 1:
            links_num = 1
        # limit upper bound for the number of links
        if links_num > nodes_num * (nodes_num - 1):
            links_num = nodes_num * (nodes_num - 1)
        # define a set of the network nodes
        for i in range(1, nodes_num + 1):
            self.nodes.append(node.Node(i))
        # generate random set of the network links
        # ! some nodes in the network could not be linked
        l_num = 0  # counter for the links number
        while l_num < links_num:
            out_node = random.choice(self.nodes)
            in_node = random.choice(self.nodes)
            while out_node is in_node:
                in_node = random.choice(self.nodes)
            if not self.contains_link(out_node, in_node):
                self.add_link(out_node.code, in_node.code, s_weight.get_value(), True)
                l_num += 1

    def gen_lines(self, lines_num, s_stops_num):
        """
            Generates specified number of lines which contain the random number of stops
            lines_num - number of lines
            s_stop_num - stochastic variable of the stops number
        """
        # line could contain more than 1 stop in the same node: an appropriate check should be added
        for idx_line in range(lines_num):
            stops_num = int(s_stops_num.get_value())
            if stops_num < 2:
                stops_num = 2
            stops = []
            stop = random.choice(self.nodes)  # begin stop
            while len(stop.out_links) == 0:
                stop = random.choice(self.nodes)
            stops.append(stop.code)
            for idx_stop in range(stops_num - 1):
                next_stop = (random.choice(stop.out_links)).in_node
                while len(next_stop.out_links) == 0 or next_stop.code in stops:
                    next_stop = (random.choice(stop.out_links)).in_node
                stop = next_stop
                stops.append(stop.code)
            self.lines.append(line.Line(self, stops))

    def dijkstra(self, source):
        # 1 function Dijkstra(Graph, source):
        # 2     dist[source]:= 0                // Distance from source to source
        # 3     for each vertex v in Graph:     // Initializations
        # 4         if v != source
        # 5             dist[v]:= infinity      // Unknown distance function from source to v
        # 6             previous[v]:= undefined // Previous node in optimal path from source
        # 7         end if
        # 8         add v to Q                  // All nodes initially in Q
        # 9     end for
        # 10
        # 11    while Q is not empty:                   // The main loop
        # 12        u:= vertex in Q with min dist[u]    // Source node in first case
        # 13        remove u from Q
        # 14
        # 15        for each neighbor v of u:           // where v has not yet been removed from Q.
        # 16            alt:= dist[u] + length(u, v)
        # 17            if alt < dist[v]:               // A shorter path to v has been found
        # 18                dist[v]:= alt
        # 19                previous[v]:= u
        # 20            end if
        # 21        end for
        # 22    end while
        # 23 return dist[], previous[]
        # 24 end function
        size = max([nd.code for nd in self.nodes])
        distance = [float('inf') for _ in range(size)]
        previous = [None for _ in range(size)]
        q = self.nodes[:]
        distance[source.code - 1] = 0
        while len(q) > 0:
            u = q[0]
            min_distance = distance[u.code - 1]
            for nd in q:
                if distance[nd.code - 1] < min_distance:
                    u = nd
                    min_distance = distance[u.code - 1]
            q.remove(u)
            neighbors = [lnk.in_node for lnk in u.out_links]
            for v in neighbors:
                alt = distance[u.code - 1] + self.get_link(u, v).weight
                if alt < distance[v.code - 1]:
                    distance[v.code - 1] = alt
                    previous[v.code - 1] = u
        return previous

    def define_path(self, source, target):
        # 1 S:= empty sequence
        # 2 u:= target
        # 3 while previous[u] is defined:       // Construct the shortest path with a stack S
        # 4     insert u at the beginning of S  // Push the vertex into the stack
        # 5     u:= previous[u]                 // Traverse from target to source
        # 6 end while
        previous = self.dijkstra(source)
        u = target
        path = []
        while previous[u.code - 1] is not None:
            path.append(u)
            u = previous[u.code - 1]
        path.reverse()
        return path

    def define_destinations(self, source, target):
        """
            Returns a list of destination nodes for the trip from source to target
            (the list includes the nodes where a passenger changes the line and the target node)
        """
        destinations = [source]
        transfers = self.transfer_nodes
        path = self.define_path(source, target)
        # print [nd.code for nd in path], "::", [nd.code for nd in transfers]
        for nd in path:
            if nd in transfers:
                destinations.append(nd)
        if target not in destinations:
            destinations.append(target)
        pos = 0
        while len(destinations) - pos > 2:
            transfer_found = True
            for ln in np.array(self.lines)[[l.contains_node(destinations[pos]) for l in self.lines]]:
                if ln.contains_node(destinations[pos + 1]) and \
                        ln.contains_node(destinations[pos + 2]):
                    destinations.remove(destinations[pos + 1])
                    transfer_found = False
                    break
            if transfer_found:
                pos += 1
        return destinations[1:]

    def gen_demand(self, duration, is_stochastic=True):
        """
            Generates demand for trips in the network
            duration - duration of the simulation period, min.
        """
        self.demand = []
        if is_stochastic:
            for source in self.nodes:
                time = round(source.s_interval.get_value(), 1)
                while time <= duration:
                    # generating a new passenger
                    new_passenger = passenger.Passenger(net=self)
                    new_passenger.m_appearance = time
                    new_passenger.origin_node = source
                    # defining the target node - random choice rule (can't be the same as origin node)
                    target = random.choice(self.nodes)
                    while target == source:
                        target = random.choice(self.nodes)
                    new_passenger.destination_nodes = self.define_destinations(source, target)
                    # print(time, [new_passenger.origin_node.code] + [nd.code for nd in new_passenger.destination_nodes])
                    new_passenger.reset() # set initial values of boarding and disembarkation times
                    # adding the passenger to the origin node collection
                    source.pass_out.append(new_passenger)
                    self.demand.append(new_passenger)
                    time += round(source.s_interval.get_value(), 1)
        else:
            # for simulations based on the defined demand (1 hour duration!)
            for nd in self.nodes:
                time = 0
                for din in nd.direct_in:
                    if din > 0:
                        st = stochastic.Stochastic(law=2, scale=60.0 / din)
                        t = st.get_value()
                        while t <= 60: # 1 hour duration only!?
                            t += st.get_value()
                            new_passenger = passenger.Passenger(net=self)
                            new_passenger.m_appearance = time + t
                            new_passenger.origin_node = nd
                            destination_node = random.choice(self.nodes)
                            find_next = True
                            while find_next:
                                if destination_node == nd:
                                    destination_node = random.choice(self.nodes)
                                    find_next = True
                                    continue
                                idx = time // 60 if time // 60 < len(nd.direct_in) else len(nd.direct_in) - 1
                                # print "sum:", sum(dnd.direct_out[idx] for dnd in self.nodes)
                                if sum(dnd.direct_out[idx] for dnd in self.nodes) - nd.direct_out[idx] >= 1:
                                    if destination_node.direct_out[idx] > 0:
                                        destination_node.direct_out[idx] -= 1
                                        find_next = False
                                    else:
                                        destination_node = random.choice(self.nodes)
                                        find_next = True
                                else:
                                    find_next = False
                            new_passenger.destination_nodes = self.define_destinations(nd, destination_node)
                            new_passenger.current_destination_node = new_passenger.destination_nodes[0]
                            nd.pass_out.append(new_passenger)
                            self.demand.append(new_passenger)
                            # print new_passenger.origin_node.code, new_passenger.destination_node.code
                        time += 60
                time = 0
                for bin in nd.back_in:
                    if bin > 0:
                        st = stochastic.Stochastic(law=2, scale=60.0 / bin)
                        t = st.get_value()
                        while t <= 60:
                            t += st.get_value()
                            new_passenger = passenger.Passenger(net=self)
                            new_passenger.m_appearance = time + t
                            new_passenger.origin_node = nd
                            destination_node = random.choice(self.nodes)
                            find_next = True
                            while find_next:
                                if destination_node == nd:
                                    destination_node = random.choice(self.nodes)
                                    find_next = True
                                    continue
                                idx = time // 60 if time // 60 < len(nd.back_in) else len(nd.back_in) - 1
                                # print "sum:", sum(dnd.direct_out[idx] for dnd in self.nodes)
                                if sum(dnd.back_out[idx] for dnd in self.nodes) - nd.back_out[idx] >= 1:
                                    if destination_node.back_out[idx] > 0:
                                        destination_node.back_out[idx] -= 1
                                        find_next = False
                                    else:
                                        destination_node = random.choice(self.nodes)
                                        find_next = True
                                else:
                                    find_next = False
                            new_passenger.destination_nodes = self.define_destinations(nd, destination_node)
                            new_passenger.current_destination_node = new_passenger.destination_nodes[0]
                            nd.pass_out.append(new_passenger)
                            self.demand.append(new_passenger)
                    time += 60

    @property
    def od_matrix(self):
        od = {}
        for origin in self.nodes:
            for destination in self.nodes:
                od[(origin.code, destination.code)] = 0
        for psg in self.demand:
            od[(psg.origin_node.code, psg.destination_nodes[-1].code)] += 1
        return od

    def print_od_matrix(self):
        od = self.od_matrix
        res = 'OD\t'
        for nd in self.nodes:
            res += str(nd.code) + '\t'
        res += '\n'
        for origin in self.nodes:
            res += str(origin.code) + '\t'
            for destination in self.nodes:
                res += str(od[(origin.code, destination.code)]) + '\t'
            res += '\n'
        print(res)

    def simulate(self, duration=8*60, time_step=1):
        """
            Simulation of the transport network
        """
        self.duration = duration
        # demand generation !!!
        # self.gen_demand(duration=self.duration, is_stochastic=True)
        # define schedules
        for ln in self.lines:
            ln.define_schedule()
            for v in ln.vehicles:
                # put zero values to the vehicle characteristics
                v.reset()
                # correct the simulation duration
                # if self.duration < v.schedule[-1][0]:
                #     self.duration = v.schedule[-1][0]
        # run the lines simulation
        self.time = 0
        while self.time <= self.duration:
            for ln in self.lines:
                ln.run()
            self.time += time_step

        # estimate total wait times
        # started_wait_time = sum([p.wait_time for p in self.demand if p.service_started])
        # finished_wait_time = sum([p.wait_time for p in self.demand if p.service_finished])
        # nss = len([p for p in self.demand if p.service_started])
        # nsf = len([p for p in self.demand if p.service_finished])
        
        # return self.total_wait_time / len(self.demand), started_wait_time / nss, finished_wait_time / nsf
        return self.total_wait_time / len(self.demand)

    def reset(self):
        # reset resulting parameters of simulations
        for psg in self.demand:
            psg.reset()
        for nd in self.nodes:
            nd.reset()
            for psg in self.demand:
                if psg.origin_node == nd:
                    nd.pass_out.append(psg)
        for ln in self.lines:
            ln.reset()

    def load_from_file(self, file_name):
        f = open(file_name, 'r')
        for data_line in f:
            data = data_line.strip().split('\t')
            track = []
            if len(data) > 3:
                coords = data[3].split(':')
                for idx in range(0, len(coords), 2):
                    track.append((float(coords[idx]), float(coords[idx + 1])))
            # print(f'{int(data[0])}-{int(data[1])}: track {track}')
            self.add_link(int(data[0]), int(data[1]), weight=float(data[2]),
                          directed=True, track=track)
        f.close()

    def load_nodes_from_file(self, file_name):
        self.nodes = []
        f = open(file_name, 'r')
        for data_line in f:
            data = data_line.split('\t')
            next_node = node.Node(code=int(data[0]), name=data[1])
            next_node.latitude = float(data[2])
            next_node.longitude = float(data[3])
            self.nodes.append(next_node)
        f.close()

    def print_characteristics(self):
        """" Print out network parameters """
        print("Links list:")
        for lnk in self.links:
            print(f"{lnk.out_node.code} - {lnk.in_node.code}: {round(lnk.weight, 2)}, ")
        print("Lines list:")
        for ln in self.lines:
            print(ln.trace_string, round(ln.line_length, 2))

