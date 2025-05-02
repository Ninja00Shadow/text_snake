import argparse

from text_snake.engine import GameEngine


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
        help="Manage game scores"
    )

    scores_parser.add_argument(
        "--list",
        action="store_false",
        help="List all scores"
    )

    return parser.parse_args()


def scores_list():
    print("=== High Scores ===")
    return


def start_game(args):
    game = GameEngine(fps=args.speed)
    game.run()


def main():
    args = parse_args()

    if args.command == "scores" and args.list:
        scores_list()
        return

    start_game(args)

if __name__ == "__main__":
    main()
