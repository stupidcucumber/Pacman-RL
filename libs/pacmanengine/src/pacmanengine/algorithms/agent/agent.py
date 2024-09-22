from abc import ABC, abstractmethod

from pacmanengine.types.maze_state import MazeState
from pacmanengine.types.mobs import Action
from pacmanengine.types.position import Position


class Agent(ABC):
    """A base class for agent that will manipulate an
    object.
    """

    @abstractmethod
    def action(self, starting_position: Position, maze_state: MazeState) -> Action:
        """Predict the next action of the mob to miximize its
        reward.

        Parameters
        ----------
        starting_position : Position
            Position where agent currently resides.
        maze_state : MazeState
            State of the maze on the current step of prediction.

        Returns
        -------
        Action
            An action that needs to be taken by the mob.
        """
        raise NotImplementedError(
            "This is an abstract method. It needs to be implemented in the child."
        )
