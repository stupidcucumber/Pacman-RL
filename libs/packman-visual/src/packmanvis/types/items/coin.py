from packmanvis.types.state import State

from .item import Item


class Coin(Item):
    def __init__(
        self,
        state: State,
        gif: str = "animations:items/gold_coin.gif",
    ) -> None:
        super(Coin, self).__init__(gif=gif, initial_state=state)
