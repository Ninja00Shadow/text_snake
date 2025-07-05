class Apple:
    def __init__(self, position):
        self.position = position

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y
