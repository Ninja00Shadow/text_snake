import os
import random
import sys

from pytimedinput import timedKey

from apple import Apple
from consts import COLS, ROWS
from snake import Snake


def random_position():
    return random.randint(0, ROWS - 1), random.randint(0, COLS - 1)


class GameEngine:
    def __init__(self):
        self.snake = Snake()
        self.apple = Apple(random_position())
        self.field = [[" "] * COLS for _ in range(ROWS)]

    def print_field(self):
        for i in range(COLS + 2):
            print("#", end="")
        print()
        for i in range(ROWS):
            print("#", end="")
            for j in range(COLS):
                print(self.field[i][j], end="")
            print("#", end="")
            print()
        for i in range(COLS + 2):
            print("#", end="")
        print()

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

    def on_move_keys(self, event):
        if event.name == "w":
            self.snake.set_direction("w")
        elif event.name == "s":
            self.snake.set_direction("s")
        elif event.name == "a":
            self.snake.set_direction("a")
        elif event.name == "d":
            self.snake.set_direction("d")
        elif event.name == "esc":
            sys.exit(0)

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

    def run(self):
        while True:
            os.system("cls")

            self.print_field()

            txt, _ = timedKey("", timeout=0.15, resetOnInput=True, allowCharacters="wasd")
            match txt:
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

            self.snake.move()
            self.update_field()
            self.check_apple()
            if self.check_collision():
                print("Game over")
                sys.exit(0)
            # time.sleep(0.15)
