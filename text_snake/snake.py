import random

from text_snake.position import Position
from text_snake.vector import Vector


class Snake:
    def __init__(self, length, boundaries):
        self._boundaries = boundaries

        self._body = [self.generate_head()]  # (x, y) coordinates
        self.generate_body(length - 1)
        self._direction = Vector(0, 0)

        self._new_block = False
        self.block_to_remove: Position | None = None

    @property
    def head(self):
        return self._body[0]

    @property
    def body(self):
        return self._body[1:]

    @property
    def tail(self):
        return self._body[-1]

    @property
    def direction(self) -> Vector:
        if self._direction == Vector(0, 0):
            return Vector(self.head.x - self.body[0].x, self.head.y - self.body[0].y)
        return self._direction

    def generate_head(self):
        x = random.randint(int(self._boundaries[0] / 4), int(self._boundaries[0] * 3 / 4))
        y = random.randint(int(self._boundaries[1] / 4), int(self._boundaries[1] * 3 / 4))
        return Position(x, y)

    def generate_body(self, length):
        to_add = length
        current_body = set(self._body)

        while to_add > 0:
            for direction in [Vector(1, 0), Vector(-1, 0), Vector(0, 1), Vector(0, -1)]:
                new_segment = self.tail + direction

                is_out_of_bounds = new_segment.x < 0 or new_segment.x >= self._boundaries[
                    0] or new_segment.y < 0 or new_segment.y >= self._boundaries[1]

                if not (is_out_of_bounds or new_segment in current_body):
                    self._body.append(new_segment)
                    current_body.add(new_segment)
                    to_add -= 1
                    break


    # TODO: Performance
    def move(self):
        if self._direction != Vector(0, 0):
            if self._new_block:
                new_head = self.head + self._direction
                self._body.insert(0, new_head)

                self._new_block = False
            else:
                self.block_to_remove = self.tail
                new_head = self.head + self._direction
                self._body.insert(0, new_head)
                self._body.pop()
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
        return self.head.x < 0 or self.head.x >= self._boundaries[0] or self.head.y < 0 or self.head.y >= \
            self._boundaries[1]

    # TODO: Performance
    def is_self_colliding(self):
        return self.head in self.body

    def __len__(self):
        return len(self._body)

    def __contains__(self, item):
        return item in self._body
