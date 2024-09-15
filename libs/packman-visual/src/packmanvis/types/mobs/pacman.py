from packmanvis.types.mobs.mob import Mob


class Pacman(Mob):
    def __init__(self, gif: str) -> None:
        super(Pacman, self).__init__(gif=gif)
