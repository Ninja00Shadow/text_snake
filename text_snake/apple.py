class Apple:
    def __init__(self, position):
        self.position = position # (x, y) coordinates

    def __getitem__(self, item):
        return self.position[item]
