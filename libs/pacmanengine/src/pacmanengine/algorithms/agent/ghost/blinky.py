from pacmanengine.algorithms.agent.ghost.ghost import GhostAgent
from pacmanengine.types.maze_state import MazeState
from pacmanengine.types.state import State


class BlinkyAgent(GhostAgent):
    """Agent for Blinky ghost (the red one)."""

    def choose_ending_state(self, ghost_state: State, maze_state: MazeState) -> State:
        return super().choose_ending_state()
