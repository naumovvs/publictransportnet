class Line:

    def __init__(self, dlt=0, itvl=0, opn=None, ipp=0.0, name=""):
        self.name = name
        self.transfer_node = None
        # schedule parameters
        self.shift = dlt
        self.interval = itvl
        self.arrivals = []
        # stochastic variable of the passengers number
        self.out_psgs_number = opn
        # part of incoming origin passengers
        self.in_psgs_part = ipp

    def define_schedule(self, duration):
        st = self.shift
        self.arrivals = []
        while st < duration:
            self.arrivals.append(st)
            st += self.interval
