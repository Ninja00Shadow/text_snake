import random
import os
import sys
import time

from pytimedinput import timedInput

ROWS = 16
COLS = 32

field = [[" "] * COLS for _ in range(ROWS)]


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


class Apple:
    def __init__(self):
        self.position = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))

    def randomize(self, snake):
        self.position = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))

        while self.position in snake:
            self.position = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))

    def __getitem__(self, item):
        return self.position[item]


def printField():
    for i in range(COLS + 2):
        print("#", end="")
    print()
    for i in range(ROWS):
        print("#", end="")
        for j in range(COLS):
            print(field[i][j], end="")
        print("#", end="")
        print()
    for i in range(COLS + 2):
        print("#", end="")
    print()


def updateField(snake, apple):
    for i in range(ROWS):
        for j in range(COLS):
            if field[i][j] == "X":
                field[i][j] = " "

    for i in range(len(snake)):
        if i == 0:
            field[snake[i][0]][snake[i][1]] = "H"
        else:
            field[snake[i][0]][snake[i][1]] = "X"

    field[apple[0]][apple[1]] = "a"


def on_move_keys(event):
    if event.name == "w":
        snake.set_direction("w")
    elif event.name == "s":
        snake.set_direction("s")
    elif event.name == "a":
        snake.set_direction("a")
    elif event.name == "d":
        snake.set_direction("d")
    elif event.name == "esc":
        sys.exit(0)


def checkCollision(snake):
    if snake[0][0] < 0 or snake[0][0] >= ROWS or snake[0][1] < 0 or snake[0][1] >= COLS:
        return True

    for i in range(1, len(snake)):
        if snake[0] == snake[i]:
            return True

    return False


def checkApple(snake, apple):
    if snake[0] == apple.position:
        apple.randomize(snake)
        snake.new_block = True


if __name__ == "__main__":
    snake = Snake()
    apple = Apple()
    updateField(snake, apple)
    # keyboard.on_press(on_move_keys)

    while True:
        os.system("cls")

        printField()

        txt,_ = timedInput("", timeout=0.15)
        match txt:
            case "w":
                snake.set_direction("w")
            case "s":
                snake.set_direction("s")
            case "a":
                snake.set_direction("a")
            case "d":
                snake.set_direction("d")
            case "q":
                sys.exit(0)

        snake.move()
        updateField(snake, apple)
        checkApple(snake, apple)
        if checkCollision(snake):
            print("Game over")
            sys.exit(0)
        # time.sleep(0.15)
