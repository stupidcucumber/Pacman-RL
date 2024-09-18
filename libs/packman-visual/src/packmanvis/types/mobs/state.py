from dataclasses import dataclass

from packmanvis.types.mobs.action import Action


@dataclass
class State:
    pos_x: int
    pos_y: int
    action: Action
