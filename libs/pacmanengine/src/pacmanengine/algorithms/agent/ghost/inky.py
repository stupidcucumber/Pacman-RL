from pacmanengine.algorithms.agent.agent import Agent
from pacmanengine.types.maze_state import MazeState
from pacmanengine.types.mobs import Action


class InkyAgent(Agent):
    """Agent for Inky ghost (the blue one)."""

    def action(self, maze_state: MazeState) -> Action:
        return super().action(maze_state)
