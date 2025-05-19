import random

from text_snake.vector import Vector


class Snake:
    def __init__(self, length, boundaries):
        self._boundaries = boundaries

        self._body = [self.generate_head()]  # (x, y) coordinates
        self.generate_body(length - 1)

        self._direction = Vector(0, 0)
        self._new_block = False
        self.block_to_remove = None

    @property
    def head(self):
        return self._body[0]

    @property
    def body(self):
        return self._body[1:]

    @property
    def direction(self) -> Vector:
        if self._direction == Vector(0, 0):
            return Vector(self.head[0] - self.body[0][0], self.head[1] - self.body[0][1])
        return self._direction

    def generate_head(self):
        x = random.randint(int(self._boundaries[0] / 4), int(self._boundaries[0] * 3 / 4))
        y = random.randint(int(self._boundaries[1] / 4), int(self._boundaries[1] * 3 / 4))
        return x, y

    def generate_body(self, length):
        random_direction = Vector(random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)]))
        correct = False
        to_add = length

        while to_add > 0:
            while not correct:
                segment = (self._body[len(self._body)-1][0] + random_direction.x, self._body[len(self._body)-1][1] + random_direction.y)

                self._body.append(segment)

                correct = not self.is_collision()

                if not correct:
                    self._body.pop()

                    random_direction = Vector(random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)]))
            correct = False
            to_add -= 1

    def move(self):
        if self._direction != Vector(0, 0):
            if self._new_block:
                body_copy = self._body[:]

                new_head = (self._body[0][0] + self._direction.x, self._body[0][1] + self._direction.y)
                body_copy.insert(0, new_head)
                self._body = body_copy

                self._new_block = False
            else:
                self.block_to_remove = self._body[-1]
                body_copy = self._body[:-1]
                new_head = (self._body[0][0] + self._direction.x, self._body[0][1] + self._direction.y)
                body_copy.insert(0, new_head)
                self._body = body_copy
        else:
            pass

    def set_direction(self, direction_vector: Vector):
        if direction_vector == self.direction.invert():
            return

        self._direction = direction_vector

    def is_head(self, position):
        return self._body[0] == position

    def is_body(self, position):
        return position in self._body[1:]

    def is_out_of_bounds(self):
        return self.head[0] < 0 or self.head[0] >= self._boundaries[0] or self.head[1] < 0 or self.head[1] >= \
            self._boundaries[1]

    def is_collision(self):
        return self.head in self.body

    def __len__(self):
        return len(self._body)

    def __contains__(self, item):
        return item in self._body
