import random
import sys
import time

from blessed import Terminal

from .apple import Apple
from .scores import update_scores
from .snake import Snake
from .vector import Vector

key_map = {
    "w": Vector(0, -1),
    "s": Vector(0, 1),
    "a": Vector(-1, 0),
    "d": Vector(1, 0),
}


def random_position(x_bounds, y_bounds):
    return random.randint(0, x_bounds - 1), random.randint(0, y_bounds - 1)


class GameEngine:
    def __init__(self, fps=30, length=5):
        self.fps = fps

        self.running = True
        self.score = 0

        self.term = Terminal()

        self.width = self.term.width
        self.height = self.term.height
        self.snake = Snake(length, (self.width, self.height))
        self.apple = Apple(random_position(self.width - 1, self.height - 1))

    def print_field(self):
        snake_head = self.snake.head
        snake_body = self.snake.body

        apple = self.apple.position

        with self.term.location(0, 0):
            for segment in snake_body:
                print(self.term.move_xy(segment[0], segment[1]) + self.term.on_darkolivegreen(" "), end="")

            print(self.term.move_xy(apple[0], apple[1]) + self.term.on_red(" "), end="")

            segment_to_remove = self.snake.block_to_remove
            if segment_to_remove:
                print(self.term.move_xy(segment_to_remove[0], segment_to_remove[1]) + self.term.on_lawngreen(" "),
                      end="")
                self.snake.block_to_remove = None

            head = ""
            direction = self.snake.direction
            if direction.is_horizontal():
                head = ":"
            elif direction.is_vertical():
                head = "\""
            print(self.term.move_xy(snake_head[0], snake_head[1]) + self.term.on_darkolivegreen(head), end="")

    def clear_field(self):
        print(self.term.on_lawngreen(self.term.clear))

    def check_collision(self):
        if self.snake.is_out_of_bounds():
            return True

        if self.snake.is_collision():
            return True

        return False

    def check_apple(self):
        if self.snake.head == self.apple.position:
            self.apple.position = random_position(self.width - 1, self.height - 1)
            self.snake._new_block = True

            self.score += 1

    def handle_input(self):
        key = self.term.inkey(timeout=0)

        if key.lower() == "q":
            self.running = False

        v = key_map.get(key.lower())
        if v: self.snake.set_direction(v)

    def game_over(self):
        print(self.term.move_xy(0, self.term.height) + self.term.on_red("Game over"), end="")
        self.running = False

        update_scores(self.score)

    def run(self):
        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor(), self.term.location():
        # with self.term.cbreak(), self.term.hidden_cursor(), self.term.location():

            self.clear_field()

            self.print_field()

            while self.running:
                current_time = time.time()

                self.handle_input()

                self.snake.move()

                self.check_apple()
                if self.check_collision():
                    self.game_over()

                self.print_field()

                frame_duration = 1. / self.fps
                elapsed = time.time() - current_time
                time_to_sleep = max(frame_duration - elapsed, 0)
                time.sleep(time_to_sleep)

            time.sleep(2)
