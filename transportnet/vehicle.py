class Vehicle:
    """
    Vehicle servicing the line
    """

    def __init__(self, capacity=40):
        # line where vehicle operates
        self.line = None
        # schedule (list of tuples <t, node>)
        self.schedule = []
        self.last_move = None
        self.servicing = {}
        self.passengers = []
        self.serviced_passengers = []
        # vehicle capacity
        self.capacity = capacity

    @property
    def occupancy(self):
        """
        Returns current occupancy
        """
        return len(self.passengers)

    @property
    def model_time(self):
        """
        Returns current model time
        """
        return self.line.net.time

    @property
    def current_position(self):
        """"
        Returns the current position at the schedule
        """
        if self.last_move is not None:
            return self.schedule.index(self.last_move)
        else:
            return -1

    @property
    def moves_number(self):
        """"
            Returns the number of moves according to the schedule
        """
        return len(self.schedule)

    @property
    def stops_left(self):
        """
            Returns nodes left till the next end stop:
            is used in order to determine, if the passenger should use the vehicle
        """
        stops = []
        pos = 0
        if self.last_move is not None:
            pos = self.current_position + 1
        if pos < self.moves_number:
            next_stop = self.schedule[pos][1]
            stops.append(next_stop)
            while next_stop not in self.line.end_stops:
                pos += 1
                next_stop = self.schedule[pos][1]
                stops.append(next_stop)
        return stops

    def set_passengers(self):
        """"
            Set passengers at the current stop
        """
        # if self.last_move is not None:  # excess condition?
        passengers = self.passengers[:]
        for psg in self.passengers:
            if psg.current_destination_node is self.last_move[1]:
                passengers.remove(psg)
                psg.m_disembarkation[psg.current_position] = self.model_time
                psg.current_destination_node.pass_in.append(psg)
                # if travel is not finished, set the next destination node
                if not psg.travel_is_finished:
                    psg.current_destination_node.pass_out.append(psg)
                    psg.current_destination_node = psg.destination_nodes[psg.current_position + 1]
                self.serviced_passengers.append(psg)
        self.passengers = passengers

    def get_passengers(self):
        """
            Get passengers at the current stop
        """
        # if self.last_move is not None:  # excess condition?
        passengers = self.last_move[1].pass_out[:]
        for psg in self.last_move[1].pass_out:
            if (psg.current_position == 0 and psg.m_appearance <= self.model_time
                or psg.current_position > 0 and psg.m_disembarkation[psg.current_position - 1] <= self.model_time) \
                    and psg.current_destination_node in self.stops_left\
                    and self.occupancy < self.capacity:
                passengers.remove(psg)
                psg.m_boarding[psg.current_position] = self.line.net.time
                psg.used_vehicles.append(self)
                self.passengers.append(psg)
            self.last_move[1].pass_out = passengers

    def move(self):
        """
            Simulate the vehicle's move to the next stop
        """
        if self.last_move is not None:
            # the schedule is not covered yet
            if self.current_position < self.moves_number - 1:
                # intermediate stops of the route
                if self.schedule[self.current_position + 1][0] <= self.model_time:
                    # moving to the next stop
                    self.last_move = self.schedule[self.current_position + 1]
                    self.set_passengers()
                    self.get_passengers()
            else:
                # route ending: self.current_position == self.moves_number
                if self.last_move[0] <= self.model_time and self.occupancy > 0:
                    self.set_passengers()
        else:
            # starting case
            if self.schedule[0][0] <= self.model_time:
                self.last_move = self.schedule[0]
                self.get_passengers()
        # passengers serviced at the current move
        self.servicing[self.last_move] = self.passengers[:]

    def reset(self):
        self.last_move = None
        self.servicing = {}
        self.passengers = []
        self.serviced_passengers = []

