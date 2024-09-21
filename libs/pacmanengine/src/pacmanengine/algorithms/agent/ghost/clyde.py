from pacmanengine.algorithms.agent.ghost.ghost import GhostAgent
from pacmanengine.types.maze_state import MazeState
from pacmanengine.types.state import State


class ClydeAgent(GhostAgent):
    """Agent for Clyde ghost (the orange one)."""

    def choose_ending_state(self, ghost_state: State, maze_state: MazeState) -> State:
        return super().choose_ending_state()
