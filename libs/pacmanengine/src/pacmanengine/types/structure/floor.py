from pacmanengine.types.animated import Animated


class Floor(Animated):
    def __init__(self, gif: str = "animations:structure/floor/floor.gif") -> None:
        super(Floor, self).__init__(gif)
