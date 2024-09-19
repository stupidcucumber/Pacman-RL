from dataclasses import dataclass


@dataclass
class EntityWeight:
    COIN_WEIGHT: int = 2
    PACMAN_WEIGHT: int = 5
    GHOST_WEIGHT: int = 11
