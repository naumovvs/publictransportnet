class Passenger:

    def __init__(self):
        self.t_appear = 0
        self.t_board = 0
        self.to_transfer = False
        self.next_line = None

    @property
    def wait_time(self):
        return self.t_board - self.t_appear

