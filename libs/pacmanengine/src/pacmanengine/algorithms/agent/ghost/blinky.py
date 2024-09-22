from pacmanengine.algorithms.agent.ghost.ghost import GhostAgent
from pacmanengine.algorithms.agent.ghost.state import GhostState
from pacmanengine.types.maze_state import MazeState
from pacmanengine.types.position import Position


class BlinkyAgent(GhostAgent):
    """Agent for Blinky ghost (the red one)."""

    def __init__(self, state: GhostState = GhostState.CHASE) -> None:
        super(BlinkyAgent, self).__init__(state=state)

    @property
    def home_position(self) -> Position:
        return Position(pos_x=0, pos_y=0)

    def choose_ending_position(
        self, ghost_position: Position, maze_state: MazeState
    ) -> Position:
        result = ghost_position

        if self.counter < 7:
            result = maze_state.pacman_position
            self.setGhostState(state=GhostState.CHASE)
        elif self.counter >= 7 and self.counter < 20:
            result = self.home_position
            self.setGhostState(state=GhostState.SCATTER)
        else:
            result = maze_state.pacman_position
            self.setGhostState(state=GhostState.CHASE)

        return result
