from __future__ import annotations

from typing import Callable

from pacmanengine.algorithms.agent.agent import Agent
from pacmanengine.types.animated import Animated
from pacmanengine.types.collidable import Collidable
from pacmanengine.types.mobs.action import Action
from pacmanengine.types.position import Position


class Mob(Animated, Collidable):
    """A class that represents a movable object.

    Parameters
    ----------
    move_right_gif : str
        GIF that will be shown when object moves right.
    move_left_gif : str
        GIF that will be shown when object moves left.
    move_up_gif : str
        GIF that will be shown when object moves up.
    move_down_gif : str
        GIF that will be shown when object moves down.
    position : Position
        Initial position of the object (x, y).
    action : Action
        Action that is currently being taken.
    agent : Agent
        Agent that controlls mob.

    Notes
    -----
    This class has an ability to move itself through an
    implemented action(...) method.

    This way you can implement an algorithm of how Ghost
    will behave itself.
    """

    def __init__(
        self,
        move_right_gif: str,
        move_left_gif: str,
        move_up_gif: str,
        move_down_gif: str,
        position: Position,
        action: Action,
        agent: Agent | None = None,
    ) -> None:
        Animated.__init__(
            self,
            gif=move_right_gif,
        )
        Collidable.__init__(self, position=position)
        self.agent = agent

        self.action_to_gif: dict[Action, str] = {
            Action.MOVE_UP: move_up_gif,
            Action.MOVE_DOWN: move_down_gif,
            Action.MOVE_LEFT: move_left_gif,
            Action.MOVE_RIGHT: move_right_gif,
        }
        self.action_to_move_slot: dict[Action, Callable[[Mob], bool] | None] = {
            Action.MOVE_UP: None,
            Action.MOVE_DOWN: None,
            Action.MOVE_LEFT: None,
            Action.MOVE_RIGHT: None,
        }
        self.on_action_changed_slot: Callable[[Action], None]
        self.on_move_end_slot: Callable[..., None] | None = None

        self.current_action = action

    def _movement_end(self) -> None:
        """Method that will be called at the end of
        movement.
        """
        self.setGif(self.action_to_gif[self.current_action])
        self.on_move_end_slot()

    def on_move(self, action: Action, slot: Callable[[Mob], bool]) -> None:
        """Callback that will be called when object will try to move.

        Parameters
        ----------
        action : Action
            Action that will be associated with the callback.
        slot : Callable[[Mob], bool]
            Callback that will be called when mooving. Callback
            must accept mob object and return whether movement is
            successful.
        """
        self.action_to_move_slot[action] = slot

    def on_move_end(self, slot: Callable[..., None]) -> None:
        """Callback that will be called at the end of the movement.

        Parameters
        ----------
        slot : Callable[..., None]
            Callback that accepts no arguments and returns no
            values.
        """
        self.on_move_end_slot = slot

    def on_action_changed(self, slot: Callable[[Action], None]) -> None:
        """Set a callback that will be called after current action of the
        mob have been changed.

        Parameters
        ----------
        slot : Callable[..., None]
            Callback that accepts Action type and returns no
            values.
        """
        self.on_action_changed_slot = slot

    def setAction(self, action: Action) -> None:
        """
        Parameters
        ----------
        action : Action
            Action to be set as the current action.
        """
        self.current_action = action
        self.on_action_changed_slot(action)

    def move(self, maze_state, action: Action | None = None) -> None:
        """Method moves object around. You either can pass a
        specific actions (e.g. simulate an agent, play yourself), or desire
        to do an algorithm (like simulate behavior of the ghost.)

        Parameters
        ----------
        maze_state : MazeState
            State of the maze at the moment of movement.
        action : Action, optional
            Action to take on the current step. If not passed will
            fallback to the algorithmic action.
        """
        if not action and not maze_state:
            raise ValueError("You must pass either maze_state or the action!")

        if not action and not self.agent:
            raise ValueError("Agent of this mob have not been initialized!")

        if not action and self.agent:
            action = self.agent.action(
                starting_position=self.current_position, maze_state=maze_state
            )

        self.setAction(action)

        self.action_to_move_slot[action](self)

        self._movement_end()
