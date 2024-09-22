from pacmanengine.types.animated import Animated
from pacmanengine.types.collidable import Collidable
from pacmanengine.types.position import Position


class Item(Animated, Collidable):
    """Class that represents an item on the map.

    Parameters
    ----------
    gif : str
        Path to the default gif to me dispayed.
    initial_position : Position
        Initial position of the item.
    """

    def __init__(self, gif: str, initial_position: Position) -> None:
        Animated.__init__(self, gif=gif)
        Collidable.__init__(self, position=initial_position)
