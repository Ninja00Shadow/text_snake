class Vector:
    """
    A class representing a 2D vector with basic operations.
    It supports initialization with either a tuple or two separate arguments,
    and provides methods for inverting the vector, checking if it is horizontal or vertical,
    and comparing vectors for equality.
    """
    def __init__(self, *args):
        """
        Initializes the vector with either a tuple (x, y) or two separate arguments.
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

    def invert(self) -> "Vector":
        """Inverts the vector."""
        return Vector(-self.x, -self.y)

    def is_horizontal(self) -> bool:
        """Checks if the vector is horizontal."""
        return self.x != 0 and self.y == 0

    def is_vertical(self) -> bool:
        """Checks if the vector is vertical."""
        return self.x == 0 and self.y != 0

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"
