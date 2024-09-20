import itertools
from dataclasses import dataclass

from packmanvis.types.maze import Maze, MazeState


@dataclass
class EnvironmentState:
    pass


class Environment:
    """Defines an environment for training RL-agent for the
    Pacman mob.

    Notes
    -----
    Class follows rules of the Gymnasium environment specifications.
    For more follow the link: https://arxiv.org/abs/2407.17032.
    """

    def __init__(self) -> None:
        self.maze = Maze(shape=(10, 20))

    def reset(self, seed: int = 42) -> EnvironmentState:
        pass

    def calculate_reward(self, maze_state: MazeState) -> float:
        pass

    def step(self) -> tuple[MazeState, float]:
        for mob in itertools.chain(self.maze.ghosts, [self.maze.pacman]):
            mob.move()
        maze_state = self.maze.state()
        reward = self.calculate_reward(maze_state)
        return self.maze.state(), reward

    def close(self) -> None:
        pass
