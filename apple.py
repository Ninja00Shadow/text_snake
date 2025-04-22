class Apple:
    def __init__(self, position):
        self.position = position

    def __getitem__(self, item):
        return self.position[item]
