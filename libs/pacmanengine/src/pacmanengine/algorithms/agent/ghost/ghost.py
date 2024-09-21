from abc import abstractmethod

import numpy as np
from pacmanengine.algorithms.agent.agent import Agent
from pacmanengine.types.maze_state import MazeState
from pacmanengine.types.mobs import Action
from pacmanengine.types.state import State


class GhostAgent(Agent):
    """Base class for all ghost agents. Provides realization of
    pathfinding algorithm.
    """

    @abstractmethod
    def choose_ending_state(self, maze_state: MazeState) -> State:
        """Decides which tile the ghost will target based on the
        movement of other ghosts and pacman position.

        Parameters
        ----------
        maze_state : MazeState
            State of the Maze, along with states of individual
            ghosts and Pacman.

        Returns
        -------
        State
            State in which ghost needs to be in.
        """
        raise NotImplementedError(
            "This method needs to be implemented in the child class."
        )

    def calculate_score_matrix(
        self, layout: np.ndarray, starting_state: State, ending_state: State
    ) -> np.ndarray:
        """Calculates score matrix for the provided layout
        to reach from the starting point to the end point.

        Parameters
        ----------
        layout : np.ndarray
        starting_state : State
        ending_state : State

        Returns
        -------
        np.ndarray
            Score matrix, for every path.

        Notes
        -----
        Score matrix is calculated according to the A* (A-star)
        algorithm. For more info visit link below:
        https://www.graphable.ai/blog/pathfinding-algorithms.
        """
        pass

    def choose_next_state(
        self, current_state: State, score_matrix: np.ndarray
    ) -> State:
        """Choses the next state to go into based on provided score matrix.

        Parameters
        ----------
        current_state : State
            Current state where the ghost resides.
        score_matrix : np.ndarray
            Calculated score matrix for all available paths.

        Returns
        -------
        State
            Next state to go into.
        """
        min_x, max_x = 0, score_matrix.shape[1] - 1
        min_y, max_y = 0, score_matrix.shape[0] - 1

        possible_states: list[State] = []
        if current_state.pos_x > min_x:
            possible_states.append(
                State(pos_x=current_state.pos_x - 1, pos_y=current_state.pos_y)
            )
        if current_state.pos_x < max_x:
            possible_states.append(
                State(pos_x=current_state.pos_x + 1, pos_y=current_state.pos_y)
            )
        if current_state.pos_y > min_y:
            possible_states.append(
                State(pos_x=current_state.pos_x, pos_y=current_state.pos_y - 1)
            )
        if current_state.pos_y < max_y:
            possible_states.append(
                State(pos_x=current_state.pos_x, pos_y=current_state.pos_y + 1)
            )

        return min(
            possible_states,
            key=lambda state, matrix=score_matrix: matrix[state.pos_y, state.pos_x],
        )

    def state_to_action(self, current_state: State, next_state: State) -> Action:
        """Converts transition from one state to another into the action.

        Parameters
        ----------
        current_state : State
            Where ghost resides now.
        next_state : State
            Where ghost needs to go.

        Returns
        -------
        Action
            Action that needs to be taken by the ghost to move from
            current state to the next state.
        """
        if current_state.pos_x - next_state.pos_x == -1:
            return Action.MOVE_RIGHT
        if current_state.pos_x - next_state.pos_x == 1:
            return Action.MOVE_LEFT
        if current_state.pos_y - next_state.pos_y == -1:
            return Action.MOVE_DOWN
        if current_state.pos_y - next_state.pos_y == 1:
            return Action.MOVE_UP
        return Action.STAY

    def action(self, starting_state: State, maze_state: MazeState) -> Action:
        ending_state = self.choose_ending_state(maze_state=maze_state)
        score_matrix = self.calculate_score_matrix(
            layout=maze_state.layout,
            starting_point=starting_state,
            ending_state=ending_state,
        )
        next_state = self.choose_next_state(
            current_state=starting_state, score_matrix=score_matrix
        )
        return self.state_to_action(current_state=starting_state, next_state=next_state)
