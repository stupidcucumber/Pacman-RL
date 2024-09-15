from packmanvis.types.animated import Animated


class Item(Animated):
    def __init__(self, gif: str) -> None:
        super(Item, self).__init__(gif)
