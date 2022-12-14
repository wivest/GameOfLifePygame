class Cell:
    
    def __init__(self, state: bool):
        
        self.state = state
        self.state_next = state
        self.state_previous = state
        self.neighbours = 0
        self.neighbours_next = 0
        self.born_condition = [3]
        self.alive_condition = [2, 3]
        self.nearby = [1, 2, 3, 4, 6, 7, 8, 9]


    def apply_generation(self):

        self.state_previous = self.state
        self.state = self.state_next
        self.neighbours = self.neighbours_next


    def set_next_generation(self):

        if self.state:
            self.state_next = self.neighbours in self.alive_condition
        else:
            self.state_next = self.neighbours in self.born_condition
