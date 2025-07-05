class Position:
    def __init__(self, *args):
        """
        Initializes the position with either a tuple (x, y) or two separate arguments.
        :param args:
        """
        if len(args) == 1:
            if isinstance(args[0], tuple):
                x, y = args[0]
            else:
                raise ValueError("Invalid argument type. Expected a tuple.")
        elif len(args) == 2:
            x, y = args
        else:
            raise ValueError("Invalid number of arguments. Expected 1 or 2.")

        self.x = x
        self.y = y

    def __add__(self, other) -> "Position":
        """Adds two positions or a position and a vector."""
        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Position(x={self.x}, y={self.y})"
