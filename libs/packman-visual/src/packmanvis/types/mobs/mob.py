from packmanvis.types.animated import Animated
from packmanvis.types.mobs.action import Action


class Mob(Animated):
    def __init__(self, gif: str) -> None:
        super(Mob, self).__init__(gif=gif)

    def action(self) -> Action:
        raise NotImplementedError("This action needs to be implemented!")
