from pacmanengine.algorithms.agent.ghost.ghost import GhostAgent
from pacmanengine.algorithms.agent.ghost.state import GhostState
from pacmanengine.types.maze_state import MazeState
from pacmanengine.types.position import Position


class InkyAgent(GhostAgent):
    """Agent for Inky ghost (the blue one)."""

    def __init__(self, state: GhostState = GhostState.SCATTER) -> None:
        super(InkyAgent, self).__init__(state=state)

    @property
    def home_position(self) -> Position:
        return Position(pos_x=0, pos_y=0)

    def choose_ending_position(
        self, ghost_position: Position, maze_state: MazeState
    ) -> Position:
        result = ghost_position

        if self.counter < 100:
            result = self.home_position
            self.setGhostState(state=GhostState.SCATTER)
        elif self.counter >= 100 and self.counter < 140:
            result = maze_state.pacman_position
            self.setGhostState(state=GhostState.CHASE)
        elif self.counter >= 140 and self.counter < 150:
            result = self.home_position
            self.setGhostState(state=GhostState.SCATTER)
        else:
            result = maze_state.pacman_position
            self.setGhostState(state=GhostState.CHASE)

        return result
