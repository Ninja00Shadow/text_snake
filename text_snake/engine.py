import random
import sys
import time

from blessed import Terminal

from .apple import Apple
from .consts import FPS
from .snake import Snake


def random_position(x_bounds, y_bounds):
    return random.randint(0, x_bounds - 1), random.randint(0, y_bounds - 1)


class GameEngine:
    def __init__(self):
        self.running = True
        self.term = Terminal()

        width, height = self.term.width, self.term.height
        self.snake = Snake((width - 1, height - 1))
        self.apple = Apple(random_position(width - 1, height - 1))

    def print_field(self):
        snake_head = self.snake.head
        snake_body = self.snake.body

        apple = self.apple.position

        with self.term.location(0, 0):
            print(self.term.move_xy(snake_head[0], snake_head[1]) + "H", end="")

            for segment in snake_body:
                print(self.term.move_xy(segment[0], segment[1]) + "X", end="")

            print(self.term.move_xy(apple[0], apple[1]) + "a", end="")

            segment_to_remove = self.snake.block_to_remove
            if segment_to_remove:
                print(self.term.move_xy(segment_to_remove[0], segment_to_remove[1]) + " ", end="")
                self.snake.block_to_remove = None

            print('', end="", flush=True)

    def clear_field(self):
        print(self.term.clear)

    def check_collision(self):
        if self.snake.is_out_of_bounds():
            return True

        if self.snake.is_collision():
            return True

        return False

    def check_apple(self):
        if self.snake.head == self.apple.position:
            self.apple.position = random_position(self.term.width - 1, self.term.height - 1)
            self.snake._new_block = True

    def handle_input(self):
        key = self.term.inkey(timeout=0)

        match key.lower():
            case "w":
                self.snake.set_direction((0, -1))
            case "s":
                self.snake.set_direction((0, 1))
            case "a":
                self.snake.set_direction((-1, 0))
            case "d":
                self.snake.set_direction((1, 0))
            case "q":
                sys.exit(0)

    def run(self):
        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor(), self.term.location():
        # with self.term.cbreak(), self.term.hidden_cursor(), self.term.location():

            print(self.term.on_blue(self.term.clear))

            self.print_field()

            print(self.term.move_xy(0, self.term.height) + self.term.on_blue("Press 'q' to quit"), end="")

            while self.running:

                current_time = time.time()

                self.handle_input()

                self.snake.move()
                self.check_apple()
                if self.check_collision(): # TODO: check before moving
                    print("Game over")
                    self.running = False

                self.print_field()

                last_frame_time = time.time()
                sleep_time = 1. / FPS - (current_time - last_frame_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)

            time.sleep(2)
