import enum


class LevelDifficulty(enum.IntEnum):
    EASY: int = 0
    MEDIUM: int = 1
    HARD: int = 2


class Environment:
    def __init__(self, n_ghosts: int = 4, difficulty: LevelDifficulty = LevelDifficulty.EASY) -> None:
        self.n_ghosts = n_ghosts
        self.difficulty = difficulty
    
    def reset(self, seed: int = 42) -> ...:
        pass
    
    def step(self, action: list) -> ...:
        pass
    
    def close(self) -> None:
        pass 