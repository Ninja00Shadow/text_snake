import argparse

from text_snake.logger import logger
from text_snake.defaults import read_defaults, write_defaults
from text_snake.engine import GameEngine
from text_snake.scores import display_scores, clear_scores

defaults = read_defaults()

def parse_args():
    parser = argparse.ArgumentParser(
        prog="snake",
        description="Console version of the Snake game",
    )
    parser.add_argument(
        "-s",
        "--speed",
        type=int,
        default=defaults["speed"],
        help="Game speed (default: 20)",
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=defaults["length"],
        help="Snake length (default: 5)",
    )
    parser.add_argument(
        "-v",
        "--vertical",
        type=float,
        default=0.8,
        help="Vertical speed multiplier (default: 0.8) (range: 0.1 to 1.0)",
    )

    subparsers = parser.add_subparsers(title="commands", dest="command")

    scores_parser = subparsers.add_parser(
        "scores",
        help="Manage game scores",
        description="Manage game scores. Without arguments, it will display the scores.",
    )

    scores_parser.add_argument(
        "-c",
        "--clear",
        action="store_true",
        help="Clear all scores"
    )

    defaults_parser = subparsers.add_parser(
        "defaults",
        help="Change default game values",
        description="Change default game values. Without arguments, it will display the current defaults.",
    )

    defaults_parser.add_argument(
        "-s",
        "--speed",
        type=int,
        help="Set the default game speed (min: 1)",
    )
    defaults_parser.add_argument(
        "-l",
        "--length",
        type=int,
        help="Set the default snake length (min: 1)",
    )

    return parser.parse_args()


def start_game(args):
    if args.vertical < 0.1 or args.vertical > 1.0:
        print("Vertical speed multiplier must be between 0.1 and 1.0.")
        return
    if args.speed < 1:
        print("Speed must be at least 1.")
        return
    if args.length < 2:
        print("Length must be at least 2.")
        return
    if args.length > 100:
        print("Length must not exceed 100.")
        return
    game = GameEngine(fps=args.speed, length=args.length, vertical=args.vertical)
    game.run()

def handle_defaults(args):
    if args.speed is None and args.length is None:
        print("Current defaults:")
        print(f"Speed: {defaults['speed']}")
        print(f"Length: {defaults['length']}")
        return

    if args.speed is not None:
        if args.speed < 1:
            print("Speed must be at least 1.")
            return
        defaults["speed"] = args.speed
    if args.length is not None:
        if args.length < 2:
            print("Length must be at least 2.")
            return
        defaults["length"] = args.length

    write_defaults(defaults)
    return

def main():
    args = parse_args()

    if args.command == "scores" and not args.clear:
        display_scores()
        return
    if args.command == "scores" and args.clear:
        clear_scores()
        return

    if args.command == "defaults":
        handle_defaults(args)
        return

    start_game(args)

if __name__ == "__main__":
    main()