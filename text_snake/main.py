import argparse

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
    scores_parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=10,
        help="Number of stored scores (default: 10)"
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
    game = GameEngine(fps=args.speed, length=args.length)
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
        if args.length < 1:
            print("Length must be at least 1.")
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