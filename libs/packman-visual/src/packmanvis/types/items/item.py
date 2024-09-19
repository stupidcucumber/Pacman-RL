from packmanvis.types.action import Action
from packmanvis.types.animated import Animated
from packmanvis.types.entity import Entity
from packmanvis.types.state import State


class Item(Animated, Entity):
    def __init__(self, gif: str, initial_state: State, action: Action) -> None:
        Animated.__init__(self, gif=gif)
        Entity.__init__(self, state=initial_state, action=action)
