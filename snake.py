class Snake:
    def __init__(self):
        self.body = [(5, 7), (5, 6), (5, 5)]
        self.direction = (0, 0)
        self.new_block = False

    def move(self):
        if self.direction != (0, 0):
            if self.new_block:
                body_copy = self.body[:]

                new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
                body_copy.insert(0, new_head)
                self.body = body_copy

                self.new_block = False
            else:
                body_copy = self.body[:-1]
                new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
                body_copy.insert(0, new_head)
                self.body = body_copy
        else:
            pass

    def set_direction(self, direction):
        if direction == "w" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif direction == "s" and self.direction != (-1, 0):
            self.direction = (1, 0)
        elif direction == "a" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif direction == "d" and self.direction != (0, -1):
            self.direction = (0, 1)

    def __len__(self):
        return len(self.body)

    def __getitem__(self, item):
        return self.body[item]
