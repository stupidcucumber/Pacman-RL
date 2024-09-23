import keyboard
from pacmanengine.algorithms.agent.agent import Agent
from pacmanengine.types.maze_state import MazeState
from pacmanengine.types.mobs import Action
from pacmanengine.types.position import Position


class PacmanAgent(Agent):
    """Base class for Pacman mob."""

    def __init__(self) -> None:
        self.next_action: Action = Action.MOVE_UP
        keyboard.on_press_key("W", lambda _: self.set_next_action(Action.MOVE_UP))
        keyboard.on_press_key("S", lambda _: self.set_next_action(Action.MOVE_DOWN))
        keyboard.on_press_key("D", lambda _: self.set_next_action(Action.MOVE_RIGHT))
        keyboard.on_press_key("A", lambda _: self.set_next_action(Action.MOVE_LEFT))

    def get_next_action(self) -> Action:
        result = self.next_action
        return result

    def set_next_action(self, action: Action) -> None:
        self.next_action = action

    def action(self, starting_position: Position, maze_state: MazeState) -> Action:
        return self.get_next_action()
