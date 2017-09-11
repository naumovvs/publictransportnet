import random
from transfernode import passenger
from stochastic import stochastic


class Node:

    def __init__(self):
        # expected intencity of incoming passengers beginning their trip in the node
        self.origin_pass_number = 0
        # probability that a passenger needs to change the line
        self.transfer_prob = 0.2
        # public transport lines in the transfer node
        self.lines = []
        #
        self.in_psgs = []
        self.out_psgs = []
        self.transfer_psgs = []
        self.transfered_psgs = []

    def get_line(self, line_name):
        res = None
        for ln in self.lines:
            if ln.name is line_name:
                res = ln
                break
        return res

    def generate_demand(self, duration):
        self.in_psgs = []
        self.out_psgs = []
        self.transfer_psgs = []
        self.transfered_psgs = []
        # define the arrival moments
        for ln in self.lines:
            ln.transfer_node = self
            ln.define_schedule(duration)
        # generate origin passengers
        st = 0
        s_int = stochastic.Stochastic(law=2, scale=60.0/self.origin_pass_number)
        while st < duration:
            st += s_int.get_value()
            psg = passenger.Passenger()
            psg.t_appear = st
            psg.to_transfer = False
            psg.next_line = random.choice(self.lines) # passengers part isn't considered
            self.in_psgs.append(psg)
        # generate out and transfer passengers
        for ln in self.lines:
            for tm in ln.arrivals:
                pn = int(ln.out_psgs_number.get_value())
                if pn < 0:
                    pn = 0
                for _ in range(pn):
                    p = passenger.Passenger()
                    p.t_appear = tm
                    p.to_transfer = random.random() < self.transfer_prob
                    if p.to_transfer:
                        line_to_transfer = random.choice(self.lines)
                        while line_to_transfer is ln:
                            line_to_transfer = random.choice(self.lines)
                        p.next_line = line_to_transfer
                        self.transfer_psgs.append(p)
                    #     print tm, ln.name, p.next_line.name
                    # else:
                    #     print tm, ln.name, "end"
                    self.out_psgs.append(p)

    def simulate(self, duration=90):
        wait_time = 0
        self.generate_demand(duration)
        # print len(self.in_psgs), len(self.transfer_psgs)
        #
        for psg in self.in_psgs:
            psg.t_board = duration
            for tm in psg.next_line.arrivals:
                if tm > psg.t_appear:
                    psg.t_board = tm
                    break
        #
        for psg in self.transfer_psgs:
            psg.t_board = duration
            for tm in psg.next_line.arrivals:
                if tm > psg.t_appear:
                    psg.t_board = tm
                    self.transfered_psgs.append(psg)
                    break
        # print len(self.out_psgs), len(self.transfer_psgs), len(self.transfered_psgs)
        for psg in self.transfered_psgs:
            # print psg.next_line.name, psg.t_appear, psg.t_board
            wait_time += psg.wait_time
        for psg in self.in_psgs:
            wait_time += psg.wait_time
        return wait_time
