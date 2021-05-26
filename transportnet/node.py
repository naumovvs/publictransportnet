from stochastic import stochastic


class Node:
    """ Node of the transport net """

    def __init__(self, code=0, name=""):
        self.code = code
        if name == "":
            self.name = "Node" + str(code)
        else:
            self.name = name
        # graph features
        self.out_links = []
        self.in_links = []
        # demand features
        self.s_interval = stochastic.Stochastic()
        # parameters of "not stochastic" demand
        self.direct_in = []
        self.direct_out = []
        self.back_in = []
        self.back_out = []
        # result parameters
        self.pass_out = []
        self.pass_in = []

    def reset(self):
        self.pass_out = []
        self.pass_in = []

