import os
import random
import sys
import time

from blessed import Terminal

from apple import Apple
from consts import COLS, ROWS, FPS
from snake import Snake


def random_position():
    return random.randint(0, ROWS - 1), random.randint(0, COLS - 1)


class GameEngine:
    def __init__(self):
        self.running = True
        self.term = Terminal()

        self.snake = Snake()
        self.apple = Apple(random_position())
        self.field = [[" "] * COLS for _ in range(ROWS)]

    def print_field(self):
        print('#'*(COLS + 2))
        for i in range(ROWS):
            print("#", end="")
            for j in range(COLS):
                print(self.field[i][j], end="")
            print("#", end="")
            print()

        print('#'*(COLS + 2))

    def clear_field(self):
        print(self.term.clear)

    def update_field(self):
        for i in range(ROWS):
            for j in range(COLS):
                if self.field[i][j] == "X":
                    self.field[i][j] = " "

        for i in range(len(self.snake)):
            if i == 0:
                self.field[self.snake[i][0]][self.snake[i][1]] = "H"
            else:
                self.field[self.snake[i][0]][self.snake[i][1]] = "X"

        print(self.apple[0], self.apple[1])
        self.field[self.apple[0]][self.apple[1]] = "a"

    def check_collision(self):
        if self.snake[0][0] < 0 or self.snake[0][0] >= ROWS or self.snake[0][1] < 0 or self.snake[0][1] >= COLS:
            return True

        for i in range(1, len(self.snake)):
            if self.snake[0] == self.snake[i]:
                return True

        return False

    def check_apple(self):
        if self.snake[0] == self.apple.position:
            self.apple.position = random_position()
            self.snake.new_block = True

    def handle_input(self):
        key = self.term.inkey(timeout=0)

        match key.lower():
            case "w":
                self.snake.set_direction("w")
            case "s":
                self.snake.set_direction("s")
            case "a":
                self.snake.set_direction("a")
            case "d":
                self.snake.set_direction("d")
            case "q":
                sys.exit(0)

    def run(self):
        with self.term.fullscreen(), self.term.cbreak():
            while self.running:

                current_time = time.time()

                self.handle_input()

                self.snake.move()
                self.update_field()
                self.check_apple()
                if self.check_collision():
                    print("Game over")
                    self.running = False

                self.clear_field()

                self.print_field()

                last_frame_time = time.time()
                sleep_time = 1. / FPS - (current_time - last_frame_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
