class Passenger:
    """
        Passenger traveling in the network
    """

    def __init__(self):
        # event moments
        self.m_appearance = 0
        self.m_boarding = []
        self.m_disembarkation = []
        # travel features
        self.origin_node = None
        self.destination_nodes = []
        self.current_destination_node = None
        self.used_vehicles = []

    @property
    def transits_number(self):
        return len(self.destination_nodes) - 1

    @property
    def travel_is_finished(self):
        return self.current_destination_node is self.destination_nodes[-1]

    @property
    def current_position(self):
        current_pos = -1
        for idx in range(len(self.destination_nodes)):
            if self.destination_nodes[idx] is self.current_destination_node:
                current_pos = idx
                break
        return current_pos

    @property
    def travel_time(self):
        return self.m_disembarkation[-1] - self.m_appearance

    @property
    def wait_time(self):
        return self.m_boarding[0] - self.m_appearance + \
               sum([self.m_boarding[i + 1] - self.m_disembarkation[i] for i in range(self.transits_number)])

    @property
    def transportation_time(self):
        return sum([self.m_disembarkation[i] - self.m_boarding[i] for i in range(len(self.destination_nodes))])

    def reset(self):
        self.m_boarding = [0 for _ in range(self.transits_number + 1)]
        self.m_disembarkation = [0 for _ in range(self.transits_number + 1)]
        self.current_destination_node = self.destination_nodes[0]
        self.used_vehicles = []

