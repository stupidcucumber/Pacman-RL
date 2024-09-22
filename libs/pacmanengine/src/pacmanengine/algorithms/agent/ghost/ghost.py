from abc import abstractmethod

import numpy as np
from pacmanengine.algorithms.agent.agent import Agent
from pacmanengine.algorithms.agent.ghost.a_star import a_star
from pacmanengine.algorithms.agent.ghost.state import GhostState
from pacmanengine.types.maze_state import MazeState
from pacmanengine.types.mobs import Action
from pacmanengine.types.position import Position


class GhostAgent(Agent):
    """Base class for all ghost agents. Provides realization of
    pathfinding algorithm.
    """

    def __init__(self, state: GhostState, counter: int = 0) -> None:
        super(GhostAgent, self).__init__()
        self.state = state
        self.counter = counter

    def increment_counter(self) -> None:
        """Increments steps counter by 1."""
        self.counter += 1

    def setGhostState(self, state: GhostState) -> None:
        """Sets ghost state to the new value."""
        self.state = state

    @property
    @abstractmethod
    def home_position(self) -> Position:
        """Home position of the ghost."""
        raise NotImplementedError(
            "This property needs to be implemented in the child class."
        )

    @abstractmethod
    def choose_ending_position(
        self, ghost_position: Position, maze_state: MazeState
    ) -> Position:
        """Decides which tile the ghost will target based on the
        movement of other ghosts and pacman position.

        Parameters
        ----------
        layout : np.ndarray
            Layout of the maze.
        ghost_position : Position
            Current position of the agent's ghost.
        maze_state : MazeState
            State of the Maze, along with positions of individual
            ghosts and Pacman.

        Returns
        -------
        Position
            Position in which ghost needs to be in.
        """
        raise NotImplementedError(
            "This method needs to be implemented in the child class."
        )

    def _find_probable_positions(
        self, current_position: Position, layout: np.ndarray
    ) -> list[Position]:
        """Algorithm for extract all possible ways to go from the current position.

        Parameters
        ----------
        current_position : Position
            Current cell where ghost resides.
        layout : np.ndarray
            Layout of the maze.

        Returns
        -------
        list[Position]
            List of positions where a Ghost can go.
        """
        min_x, max_x = 0, layout.shape[1] - 1
        min_y, max_y = 0, layout.shape[0] - 1
        probable_positions: list[Position] = []

        if current_position.pos_x > min_x:
            probable_positions.append(
                Position(pos_x=current_position.pos_x - 1, pos_y=current_position.pos_y)
            )
        if current_position.pos_x < max_x:
            probable_positions.append(
                Position(pos_x=current_position.pos_x + 1, pos_y=current_position.pos_y)
            )
        if current_position.pos_y > min_y:
            probable_positions.append(
                Position(pos_x=current_position.pos_x, pos_y=current_position.pos_y - 1)
            )
        if current_position.pos_y < max_y:
            probable_positions.append(
                Position(pos_x=current_position.pos_x, pos_y=current_position.pos_y + 1)
            )

        return probable_positions

    def choose_next_position(
        self, current_position: Position, ending_position: Position, layout: np.ndarray
    ) -> Position:
        """Choses the next position to go into based on provided score matrix.

        Parameters
        ----------
        current_position : Position
            Current position where the ghost resides.
        ending_position : Position
            Ending position where ghost is heading.
        layout : np.ndarray
            Layout of the maze

        Returns
        -------
        Position
            Next position to go into.
        """
        next_y, next_x = a_star(
            start=(current_position.pos_y, current_position.pos_x),
            goal=(ending_position.pos_y, ending_position.pos_x),
            layout=layout,
        )
        return Position(pos_x=next_x, pos_y=next_y)

    def position_to_action(
        self, current_position: Position, next_position: Position
    ) -> Action:
        """Converts transition from one position to another into the action.

        Parameters
        ----------
        current_position : Position
            Where ghost resides now.
        next_position : Position
            Where ghost needs to go.

        Returns
        -------
        Action
            Action that needs to be taken by the ghost to move from
            current position to the next position.
        """
        if current_position.pos_x - next_position.pos_x == -1:
            return Action.MOVE_RIGHT
        if current_position.pos_x - next_position.pos_x == 1:
            return Action.MOVE_LEFT
        if current_position.pos_y - next_position.pos_y == -1:
            return Action.MOVE_DOWN
        if current_position.pos_y - next_position.pos_y == 1:
            return Action.MOVE_UP
        return Action.STAY

    def action(self, starting_position: Position, maze_state: MazeState) -> Action:
        ending_position = self.choose_ending_position(
            ghost_position=starting_position, maze_state=maze_state
        )
        next_position = self.choose_next_position(
            current_position=starting_position,
            ending_position=ending_position,
            layout=maze_state.layout,
        )
        self.increment_counter()
        return self.position_to_action(
            current_position=starting_position, next_position=next_position
        )
