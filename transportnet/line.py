class Line:
    """
        Public transport line
    """

    def __init__(self, net, codes, end_codes=[]):
        # route configuration
        self.net = net
        self.nodes = []
        # checking the route correctness
        if len(codes) < 2:
            raise Exception("Line should contain at least 2 nodes.")
        for code in codes:
            if net.contains_node(code):
                self.nodes.append(self.net.get_node(code))
            else:
                raise Exception("No such a node in the net: ", code)
        for idx in range(len(self.nodes) - 1):
            out_node = self.nodes[idx]
            in_node = self.nodes[idx + 1]
            if not net.contains_link(out_node, in_node):
                raise Exception("No such a link in the net: ",
                                str(out_node.code) + " - " + str(in_node.code))
        # collection of vehicles operating at the line
        self.vehicles = []
        # schedule parameters [min]
        self.nodes_sequence = []
        self.schedule_shift = 0
        self.end_stop_duration = 5
        self.intermediate_stop_duration = 1
        self.end_stops = []
        if len(end_codes) < 2:
            self.end_stops = [self.nodes[0], self.nodes[-1]]
        else:
            self.end_stops = [self.net.get_node(end_codes[0]), self.net.get_node(end_codes[-1])]
        # mean velocity of buses at the line [km/h]
        self.velocity = 25

    def __str__(self):
        res = 'Line: '
        for nd in self.nodes:
            res += str(nd.code) + ' '
        return res

    @property
    def line_length(self):
        """
            Returns the line length in both directions [km]
        """
        length = 0
        for idx in range(len(self.nodes) - 1):
            out_node = self.nodes[idx]
            in_node = self.nodes[idx + 1]
            length += self.net.get_link(out_node, in_node).weight
        return length

    @property
    def trace_string(self):
        """" Returns the line trace as a sequence of nodes: a string containing the codes of the nodes """
        t_str = str(self.nodes[0].code) + " - "
        if len(self.nodes) > 2:
            for idx in range(1, len(self.nodes) - 1):
                t_str += str(self.nodes[idx].code) + " - "
        t_str += str(self.nodes[-1].code)
        return t_str

    @property
    def turnaround_time(self):
        """" Returns the line turnaround duration [min] """
        return 60 * self.line_length / self.velocity + \
               self.intermediate_stop_duration * (len(self.nodes) - 2) + \
               2 * self.end_stop_duration

    @property
    def turns_number(self):
        """" Returns the possible number of turns during the simulation period """
        return int(self.net.duration / self.turnaround_time) + 1

    @property
    def nodes_reversed(self):
        """" Returns the list of the line stops (their codes) in the reversed order """
        nds = []
        for i in range(len(self.nodes) - 1, -1, -1):
            nds.append(self.nodes[i])
        return nds

    def define_sequence(self, turns, same_trace=True):
        """
        returns the sequence of nodes passed by vehicles during the simulation period
        """
        nds = []
        nds.extend(self.nodes[:-1])
        for tn in range(self.turns_number - 1):
            if same_trace:
                nds.extend(self.nodes_reversed)
                nds.extend(self.nodes[1:-1])
            else:
                nds.extend(self.nodes[:-1])
        if same_trace:
            nds.extend(self.nodes_reversed)
        else:
            nds.append(self.nodes[-1])
        self.nodes_sequence = nds

    def define_schedule(self):
        """
            Defines the line schedule
        """
        interval = round(self.turnaround_time / len(self.vehicles), 0)
        self.define_sequence(self.turns_number, same_trace=True)  # the same trace in back direction
        t0 = self.schedule_shift
        for vhcl in self.vehicles:
            # defining start parameters of the vehicle's schedule
            vhcl.schedule = []
            vhcl.last_move = None
            # adding start point to the schedule
            st = t0
            vhcl.schedule.append((st, self.nodes_sequence[0]))
            # time shift for the first stop
            st -= self.end_stop_duration
            # calculating the moments of arrivals to the line stops
            for idx in range(1, len(self.nodes_sequence)):
                if self.nodes_sequence[idx - 1] in self.end_stops:
                    st += self.end_stop_duration
                else:
                    st += self.intermediate_stop_duration
                lnk = self.net.get_link(self.nodes_sequence[idx - 1],
                                        self.nodes_sequence[idx])
                st += round(60 * lnk.weight / self.velocity, 0)
                vhcl.schedule.append((st, self.nodes_sequence[idx]))
            # time shift for the next vehicle
            t0 += interval

    def add_vehicles(self, vehicles):
        """
        Adds vehicles to run on the line
        """
        for vehicle in vehicles:
            vehicle.line = self
            self.vehicles.append(vehicle)

    def contains_node(self, nd):
        return nd in self.nodes

    def run(self):
        """
        Runs the process of line simulation
        """
        for vhcl in self.vehicles:
            vhcl.move()

    def reset(self):
        self.nodes_sequence = []
        self.schedule_shift = 0
