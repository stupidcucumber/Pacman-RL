from pacmanengine.types.position import Position

from .item import Item


class Coin(Item):
    def __init__(
        self,
        position: Position,
        gif: str = "animations:items/gold_coin.gif",
    ) -> None:
        super(Coin, self).__init__(gif=gif, initial_position=position)
