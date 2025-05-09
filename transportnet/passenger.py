class Passenger:
    """
        Passenger traveling in the network
    """

    def __init__(self, net=None):
        self.net = net
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
    def travel_to_be_finished(self):
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
        """
            Returns the total travel time since the appearance in the origin node
        """
        if self.service_finished:
            return self.m_disembarkation[-1] - self.m_appearance
        else:
            return self.net.duration - self.m_appearance

    @property
    def ride_time(self):
        """
            Returns the total in-vehicle time
        """
        rt = 0
        for i in range(self.transits_number + 1):
            if self.m_disembarkation[i] >= self.m_boarding[i]:
                rt += self.m_disembarkation[i] - self.m_boarding[i]
            else: # on the way to the next stop at the moment of the simulations termination
                rt += self.net.duration - self.m_boarding[i]
        return rt

    @property
    def wait_time(self):
        """
            Returns the total wait time
        """
        wt = 0
        if self.m_boarding[0] > 0:
            wt = self.m_boarding[0] - self.m_appearance
        else:
            return self.net.duration - self.m_appearance
        for i in range(self.transits_number):
            if self.m_boarding[i + 1] >= self.m_disembarkation[i]:
                wt += self.m_boarding[i + 1] - self.m_disembarkation[i]
            else: # waiting in the next stop at the moment of the simulations termination
                wt += self.net.duration - self.m_disembarkation[i]
                break
        return wt

    @property
    def service_started(self):
        return self.m_boarding[0] > self.m_appearance
    
    @property
    def service_finished(self):
        return self.m_disembarkation[-1] > self.m_appearance

    def reset(self):
        self.m_boarding = [0 for _ in range(self.transits_number + 1)]
        self.m_disembarkation = [0 for _ in range(self.transits_number + 1)]
        self.current_destination_node = self.destination_nodes[0]
        self.used_vehicles = []

