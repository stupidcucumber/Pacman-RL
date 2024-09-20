from packmanvis.types.animated import Animated
from packmanvis.types.collidable import Collidable
from packmanvis.types.state import State


class Item(Animated, Collidable):
    """Class that represents an item on the map.

    Parameters
    ----------
    gif : str
        Path to the default gif to me dispayed.
    initial_state : State
        Initial state of the item.
    """

    def __init__(self, gif: str, initial_state: State) -> None:
        Animated.__init__(self, gif=gif)
        Collidable.__init__(self, state=initial_state)
