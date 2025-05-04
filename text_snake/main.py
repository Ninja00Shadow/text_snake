import argparse

from text_snake.engine import GameEngine
from text_snake.scores import display_scores, clear_scores


def parse_args():
    parser = argparse.ArgumentParser(
        prog="snake",
        description="Console version of the Snake game",
    )
    parser.add_argument(
        "--speed",
        type=int,
        default=30,
        help="Game speed in frames per second (default: 30)"
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

    return parser.parse_args()


def start_game(args):
    game = GameEngine(fps=args.speed)
    game.run()


def main():
    args = parse_args()

    if args.command == "scores" and not args.clear:
        display_scores()
        return
    if args.command == "scores" and args.clear:
        clear_scores()
        return

    start_game(args)

if __name__ == "__main__":
    main()
