from .item import Item


class Coin(Item):
    def __init__(self, gif: str = "animations:items/gold_coin.gif") -> None:
        super(Item, self).__init__(gif=gif)
