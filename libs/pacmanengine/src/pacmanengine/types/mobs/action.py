import enum


class Action(enum.IntEnum):
    """Enum class that registers available actions
    an Entity can take.

    Attributes
    ----------
    MOVE_UP : int, default=1
        Move one cell upwards.
    MOVE_DOWN : int, default=2
        Move one cell downwards.
    MOVE_LEFT : int, default=3
        Move one cell to the left.
    MOVE_RIGHT : int, default=4
        Move one cell to the right.
    STAY : int, default=5
        Stay in the same cell.
    """

    MOVE_UP: int = 1
    MOVE_DOWN: int = 2
    MOVE_LEFT: int = 3
    MOVE_RIGHT: int = 4
    STAY: int = 5
