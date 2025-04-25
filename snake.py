import random


class Snake:
    def __init__(self, boundaries):
        self._boundaries = boundaries

        self._body = [self.generate_head()]  # (x, y) coordinates
        self.generate_body()

        self._direction = (0, 0)
        self._new_block = False
        self.block_to_remove = None

    @property
    def head(self):
        return self._body[0]

    @property
    def body(self):
        return self._body[1:]

    def generate_head(self):
        x = random.randint(int(self._boundaries[0] / 4), int(self._boundaries[0] * 3 / 4))
        y = random.randint(int(self._boundaries[1] / 4), int(self._boundaries[1] * 3 / 4))
        return x, y

    def generate_body(self):
        last_segment = self._body[0]

        random_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        correct = False
        while not correct:
            first_segment = (last_segment[0] + random_direction[0], last_segment[1] + random_direction[1])
            second_segment = (last_segment[0] + random_direction[0] * 2, last_segment[1] + random_direction[1] * 2)

            self._body.append(first_segment)
            self._body.append(second_segment)

            correct = not self.is_collision()

            if not correct:
                self._body.pop()
                self._body.pop()

                random_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def move(self):
        if self._direction != (0, 0):
            if self._new_block:
                body_copy = self._body[:]

                new_head = (self._body[0][0] + self._direction[0], self._body[0][1] + self._direction[1])
                body_copy.insert(0, new_head)
                self._body = body_copy

                self._new_block = False
            else:
                self.block_to_remove = self._body[-1]
                body_copy = self._body[:-1]
                new_head = (self._body[0][0] + self._direction[0], self._body[0][1] + self._direction[1])
                body_copy.insert(0, new_head)
                self._body = body_copy
        else:
            pass

    def set_direction(self, direction_vector):
        last_vector_direction = (0, 0)
        dx, dy = self._direction
        if dx != 0:
            last_vector_direction = (1 if dx > 0 else -1, 0)
        if dy != 0:
            last_vector_direction = (last_vector_direction[0],
                                     1 if dy > 0 else -1)

        if direction_vector == last_vector_direction:
            self._direction = (dx + direction_vector[0], dy + direction_vector[1])
            return

        if last_vector_direction != (0, 0):
            opp_x = direction_vector[0] == -last_vector_direction[0]
            opp_y = direction_vector[1] == -last_vector_direction[1]
            if opp_x or opp_y:
                new_dx = dx + direction_vector[0]
                new_dy = dy + direction_vector[1]
                if (new_dx, new_dy) != (0, 0):
                    self._direction = (new_dx, new_dy)
                return

        next_head = (self.head[0] + direction_vector[0], self.head[1] + direction_vector[1])
        if next_head not in self._body:
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
