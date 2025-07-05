class Apple:
    def __init__(self, position):
        self.position = position # (x, y) coordinates

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y
