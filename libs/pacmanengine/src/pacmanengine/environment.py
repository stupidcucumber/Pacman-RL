import itertools
from dataclasses import dataclass

from pacmanengine.types.maze import Maze, MazeState
from pacmanengine.types.mobs import Action


@dataclass
class EnvironmentStep:
    action: Action
    maze_state: MazeState
    reward: int
    done: bool


class Environment:
    """Defines an environment for training RL-agent for the
    Pacman mob.

    Notes
    -----
    Class follows rules of the Gymnasium environment specifications.
    For more follow the link: https://arxiv.org/abs/2407.17032.
    """

    def __init__(self, shape: tuple[int, int] = (10, 20), seed: int = 42) -> None:
        self.seed = seed
        self.shape = shape
        self.maze = Maze(shape=self.shape)

    def reset(self) -> EnvironmentStep:
        """Resets the environment:
            - Recreates maze.
            - Respawns all objects in the maze.

        Returns
        -------
        EnvironmentStep
            Step of the environment.
        """
        self.maze = Maze(shape=self.shape)

    def calculate_reward(self, maze_state: MazeState) -> float:
        """Calculates the reward of the maze.

        Parameters
        ----------
        maze_state : MazeState
            State of the maze to calculate reward on.

        Returns
        -------
        float
            Calculated reward for the agent.
        """
        pass

    def step(self) -> EnvironmentStep:
        """Makes environment step (moves objects, predicts next
        best move for Pacman).

        Returns
        -------
        EnvironmentStep
            Step of the environment.
        """
        for mob in itertools.chain(self.maze.ghosts, [self.maze.pacman]):
            mob.move()
        maze_state = self.maze.state()
        return EnvironmentStep(
            reward=self.calculate_reward(maze_state),
            maze_state=maze_state,
            action=...,
            done=...,
        )
