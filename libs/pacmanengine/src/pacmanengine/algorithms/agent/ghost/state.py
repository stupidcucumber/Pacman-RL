import enum


class GhostState(enum.IntEnum):
    SCATTER: int = 0
    CHASE: int = 1
    FRIGHTENED: int = 2
