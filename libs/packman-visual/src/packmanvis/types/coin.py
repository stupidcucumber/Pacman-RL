from .entity import Entity


class Coin(Entity):
    def __init__(self, gif: str = "animations:gold_coin.gif") -> None:
        super(Entity, self).__init__(gif=gif)
