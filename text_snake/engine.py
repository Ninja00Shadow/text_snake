import random
import sys
import time

from blessed import Terminal

from .animations import box_collapse
from .logger import logger
from .apple import Apple
from .position import Position
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
    return Position(random.randint(0, x_bounds - 1), random.randint(0, y_bounds - 1))


class GameEngine:
    def __init__(self, fps=20, length=5, vertical=1.0):
        self.fps = fps

        self.running = True
        self.score = 0
        self.start_length = length

        self.term = Terminal()

        self.width = self.term.width
        self.height = self.term.height
        self.snake = Snake(length, (self.width, self.height))
        self.apple = Apple(self.generate_correct_apple_position())

        self.vertical = False
        self.vertical_multiplier = vertical

    def print_field(self):
        snake_head = self.snake.head
        snake_body = self.snake.body

        apple = self.apple.position

        with self.term.location(0, 0):
            for segment in snake_body:
                sys.stdout.write(self.term.move_xy(segment.x, segment.y) + self.term.on_darkolivegreen(" "))

            sys.stdout.write(self.term.move_xy(apple.x, apple.y) + self.term.on_red(" "))

            segment_to_remove = self.snake.block_to_remove
            if segment_to_remove:
                sys.stdout.write(self.term.move_xy(segment_to_remove.x, segment_to_remove.y) + self.term.on_lawngreen(" "))
                self.snake.block_to_remove = None

            head = ""
            direction = self.snake.direction
            if direction.is_horizontal():
                head = ":"
            elif direction.is_vertical():
                head = "\""
            sys.stdout.write(self.term.move_xy(snake_head.x, snake_head.y) + self.term.on_darkolivegreen(head))

        sys.stdout.flush()

    def clear_field(self):
        print(self.term.on_lawngreen(self.term.clear))

    def check_collision(self):
        if self.snake.is_out_of_bounds():
            logger.debug("Out of bounds collision detected.")
            return True

        if self.snake.is_self_colliding():
            logger.debug("Self-collision detected.")
            return True

        return False

    def generate_correct_apple_position(self):
        snake_positions = set(self.snake.body + [self.snake.head])
        new_position = random_position(self.width - 1, self.height - 1)
        while new_position in snake_positions:
            new_position = random_position(self.width - 1, self.height - 1)
        return new_position

    def check_apple(self):
        if self.snake.head == self.apple.position:
            self.apple.position = self.generate_correct_apple_position()
            self.snake._new_block = True

            self.score += 1

    def handle_input(self):
        key = self.term.inkey(timeout=0)

        if key.lower() == "q":
            self.running = False

        v = key_map.get(key.lower())
        if v:
            self.snake.set_direction(v)
            if self.snake.direction.is_vertical():
                self.vertical = True
            else:
                self.vertical = False

    def restart(self):
        self.running = True
        self.score = 0

        self.width = self.term.width
        self.height = self.term.height

        self.snake = Snake(self.start_length, (self.width, self.height))
        self.apple = Apple(self.generate_correct_apple_position())
        self.clear_field()
        self.print_field()

    def game_over(self):
        end_message = ("Game over!", f"Score: {self.score}", f"Restart: r", f"Quit: q")

        print(self.term.move_xy(0, self.term.height // 2 - 3))
        print(self.term.center("#" * 15))
        for line in end_message:
            print(self.term.center("# {:<11} #".format(line)))
        print(self.term.center("#" * 15))

        sys.stdout.flush()
        self.running = False

        update_scores(self.score)

        key = ''

        while key.lower() not in ("r", "q"):
            key = self.term.inkey()

            if key.lower() == "r":
                self.restart()
            elif key.lower() == "q":
                sys.exit()

    def run(self):
        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor(), self.term.location():
            self.clear_field()

            self.print_field()

            while self.running:
                current_time = time.time()

                self.handle_input()

                self.snake.move()

                self.check_apple()
                if self.check_collision():
                    box_collapse(self.term)
                    self.game_over()
                else:
                    self.print_field()

                frame_duration = 1. / (max(self.fps, 1) * (self.vertical_multiplier if self.vertical else 1.0))
                logger.debug(f"Frame duration: {frame_duration:.3f} seconds, direction: {self.snake.direction}")
                elapsed = time.time() - current_time
                time_to_sleep = max(frame_duration - elapsed, 0)
                time.sleep(time_to_sleep)
