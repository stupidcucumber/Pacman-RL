from abc import abstractmethod

import numpy as np
from pacmanengine.algorithms.agent.agent import Agent
from pacmanengine.algorithms.agent.ghost.a_star import a_star
from pacmanengine.types.maze_state import MazeState
from pacmanengine.types.mobs import Action
from pacmanengine.types.state import State


class GhostAgent(Agent):
    """Base class for all ghost agents. Provides realization of
    pathfinding algorithm.
    """

    @abstractmethod
    def choose_ending_state(self, ghost_state: State, maze_state: MazeState) -> State:
        """Decides which tile the ghost will target based on the
        movement of other ghosts and pacman position.

        Parameters
        ----------
        ghost_state : State
            Current state of the agent's ghost.
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

    def _find_probable_states(
        self, current_state: State, layout: np.ndarray
    ) -> list[State]:
        """Algorithm for extract all possible ways to go from the current state.

        Parameters
        ----------
        current_state : State
            Current cell where ghost resides.
        layout : np.ndarray
            Layout of the maze.

        Returns
        -------
        list[State]
            List of states where a Ghost can go.
        """
        min_x, max_x = 0, layout.shape[1] - 1
        min_y, max_y = 0, layout.shape[0] - 1
        probable_states: list[State] = []

        if current_state.pos_x > min_x:
            probable_states.append(
                State(pos_x=current_state.pos_x - 1, pos_y=current_state.pos_y)
            )
        if current_state.pos_x < max_x:
            probable_states.append(
                State(pos_x=current_state.pos_x + 1, pos_y=current_state.pos_y)
            )
        if current_state.pos_y > min_y:
            probable_states.append(
                State(pos_x=current_state.pos_x, pos_y=current_state.pos_y - 1)
            )
        if current_state.pos_y < max_y:
            probable_states.append(
                State(pos_x=current_state.pos_x, pos_y=current_state.pos_y + 1)
            )

        return probable_states

    def choose_next_state(
        self, current_state: State, ending_state: State, layout: np.ndarray
    ) -> State:
        """Choses the next state to go into based on provided score matrix.

        Parameters
        ----------
        current_state : State
            Current state where the ghost resides.
        layout : np.ndarray
            Layout of the maze

        Returns
        -------
        State
            Next state to go into.
        """
        next_y, next_x = a_star(start=current_state, goal=ending_state, layout=layout)
        return State(pos_x=next_x, pos_y=next_y)

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
        ending_state = self.choose_ending_state(
            ghost_state=starting_state, maze_state=maze_state
        )
        next_state = self.choose_next_state(
            current_state=starting_state, ending_state=ending_state
        )
        return self.state_to_action(current_state=starting_state, next_state=next_state)
