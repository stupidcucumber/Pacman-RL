from pacmanengine.algorithms.agent.ghost.ghost import GhostAgent
from pacmanengine.types.maze_state import MazeState
from pacmanengine.types.position import Position


class InkyAgent(GhostAgent):
    """Agent for Inky ghost (the blue one)."""

    def choose_ending_position(
        self, ghost_position: Position, maze_state: MazeState
    ) -> Position:
        return super().choose_ending_position(ghost_position, maze_state)
