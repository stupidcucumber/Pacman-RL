from .item import Item


class Coin(Item):
    def __init__(self, gif: str = "animations:gold_coin.gif") -> None:
        super(Item, self).__init__(gif=gif)
