class Link:
    """ Link between the net nodes """

    def __init__(self, out_node, in_node, weight=0.0):
        # type: (Node, Node, float) -> Link
        self.out_node = out_node
        self.in_node = in_node
        self.track = [] # list of tuples: [(lat1, lng1), (lat2, lng2), ...]
        self.lines_number = 1
        # link length [km]
        self.weight = weight
        self.capacity = 0
        self.load = 0

    def __str__(self):
        return f'({self.out_node.code}-{self.in_node.code})'


