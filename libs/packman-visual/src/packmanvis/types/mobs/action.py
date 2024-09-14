import enum


class Action(enum.IntEnum):
    MOVE_UP: int = 0
    MOVE_DOWN: int = 1
    MOVE_LEFT: int = 2
    MOVE_RIGHT: int = 3