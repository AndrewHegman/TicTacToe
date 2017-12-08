class Agent:
    def __init__(self, number, is_human):
        self.number = number
        self.is_human = is_human

    def request_move(self):
        return int(input("Please type the position you would like to play: "))




