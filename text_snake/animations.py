import sys
import time


def box_collapse(term):
    screen_width, screen_height = term.width, term.height
    animation_steps = 5
    step_x = max(1, (screen_width + 1) // (animation_steps * 2))
    step_y = max(1, (screen_height + 1) // (animation_steps * 2))

    sys.stdout.write(term.home)
    for step in range(animation_steps):
        offset_x = step_x * step
        offset_y = step_y * step

        inner_width = screen_width - offset_x - step_x
        inner_height = screen_height - offset_y - step_y
        if inner_width <= 0 or inner_height <= 0:
            break

        for y in range(step_y):
            x_start = offset_x + step_x
            y_start_top = offset_y + y
            y_start_bottom = screen_height - 1 - offset_y - y

            sys.stdout.write(term.move_xy(x_start, y_start_top) + " " * inner_width)
            sys.stdout.write(term.move_xy(x_start, y_start_bottom) + " " * inner_width)

        for y in range(screen_height - offset_y):
            y_start = offset_y + y
            left_x = offset_x
            right_x = inner_width

            sys.stdout.write(term.move_xy(left_x, y_start) + " " * step_x)
            sys.stdout.write(term.move_xy(right_x, y_start) + " " * step_x)

        sys.stdout.flush()
        time.sleep(0.3)

    sys.stdout.write(term.clear + term.home)
    sys.stdout.flush()