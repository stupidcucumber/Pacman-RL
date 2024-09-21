from abc import ABC, abstractmethod

from pacmanengine.types.maze_state import MazeState
from pacmanengine.types.mobs import Action
from pacmanengine.types.state import State


class Agent(ABC):
    """A base class for agent that will manipulate an
    object.
    """

    @abstractmethod
    def action(self, starting_state: State, maze_state: MazeState) -> Action:
        """Predict the next action of the mob to miximize its
        reward.

        Parameters
        ----------
        starting_state : State
            State from where agent currently resides.
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
