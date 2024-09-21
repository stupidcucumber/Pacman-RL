from collections import deque
from dataclasses import dataclass
from typing import Callable

import numpy as np
from pacmanengine.algorithms.maze import generate_pacmanlike_maze
from pacmanengine.algorithms.maze.types import EntityWeight
from pacmanengine.types.collidable import Collidable
from pacmanengine.types.items import Coin
from pacmanengine.types.maze_state import MazeState
from pacmanengine.types.mobs import Action, Ghost, GhostType, Mob, Pacman
from pacmanengine.types.state import State

from .animated import Animated
from .structure import Floor, Wall, WallType


@dataclass
class Tile:
    """Object that represents a single cell on the
    map.

    Attributes
    ----------
    objects : list[Animated]
        A list of objects that tile contains.
    """

    objects: list[Animated]

    @property
    def is_wall(self) -> bool:
        """Checks whether the current tile contains wall as the
        first object. If so, then True is returned.
        """
        return isinstance(self.objects[0], Wall)

    def pop(self, obj: Animated) -> None:
        """Removes object from the cell.

        Parameters
        ----------
        obj : Animated
            An object to be removed from the cell.
        """
        self.objects.remove(obj)

    def append(self, obj: Animated) -> bool:
        """Places object at the top of the cell if
        cell does not contain wall.

        Parameters
        ----------
        obj : Animated
            Object to be placed.

        Returns
        -------
        bool
            True if object is successfully been placed onto
            the tile, otherwise returns False.
        """
        if self.is_wall:
            return False
        self.objects.append(obj)
        return True


class Maze:
    """An oracle object that defines rules of the game
    and constructs a map.

    It is responsible for generating maze, populating it with
    structures/mobs/items. It also provides an interface to access
    internal part of the maze.

    Parameters
    ----------
    shape : tuple[int, int]
        Shape of the maze.
    """

    def __init__(self, shape: tuple[int, int]) -> None:
        self.ghosts: list[Ghost] = []
        self.pacman: Pacman | None = None
        self.score: int = 0
        self.hearts: int = 3

        self.layout = generate_pacmanlike_maze(shape=shape)
        self.nrows = self.layout.shape[0]
        self.ncols = self.layout.shape[1]
        self.tiles: list[Tile] = self._layout_from_map(self.layout)

        self.on_score_changed_slot: Callable[[], None] | None = None
        self.on_hearts_changed_slot: Callable[[], None] | None = None

    def on_score_changed(self, slot: Callable[[], None]) -> None:
        self.on_score_changed_slot = slot

    def on_hearts_changed(self, slot: Callable[[], None]) -> None:
        self.on_hearts_changed_slot = slot

    def _move_object(self, obj: Mob, delta_x: int, delta_y: int) -> bool:
        new_state = State(
            obj.current_state.pos_x + delta_x, obj.current_state.pos_y + delta_y
        )

        if new_state.pos_x < 0 or new_state.pos_x >= self.ncols:
            return False

        if new_state.pos_y < 0 or new_state.pos_y >= self.nrows:
            return False

        next_tile = self.tile(x=new_state.pos_x, y=new_state.pos_y)

        if next_tile.append(obj):
            previous_tile = self.tile(obj.current_state.pos_x, obj.current_state.pos_x)
            previous_tile.pop(obj)
            obj.setState(new_state)
            for collision_obj in next_tile.objects:
                obj.collision(collision_obj)
            return True
        return False

    def setScore(self, score: int) -> None:
        """Set the current score.

        Parameters
        ----------
        score : int
            Must be more or equal to 0.
        """
        if score < 0:
            return
        self.score = score
        self.on_score_changed_slot()

    def setHearts(self, hearts: int) -> None:
        """Set the number of hearts.

        Parameters
        ----------
        hearts : int
            The number of hearts. Must be more or equal to 0.
        """
        if hearts < 0:
            return
        self.hearts = hearts
        self.on_hearts_changed_slot()

    def destroy(self, obj: Collidable) -> None:
        """Completely removes object from the map.

        Parameters
        ----------
        obj : Collidable
            An object to be completely removed from the map.
        """
        self.tile(obj.current_state.pos_x, obj.current_state.pos_y).pop(obj)
        obj.destroy()

    def consume_coin(self, coin: Coin) -> None:
        """Consumes coin, which means it will be deleted from
        map and score will be increased by 50 points.

        Parameters
        ----------
        coin : Coin
            A coin to be consumed.
        """
        self.setScore(self.score + 50)
        self.destroy(coin)

    def _initialize_movement_callbacks(self, mob: Mob) -> None:
        """Initializes four basic movement callbacks inplace:
            - move left
            - move right
            - move down
            - move up

        Parameters
        ----------
        mob : Mob
            An object that needs movement callbacks to be initialized.
        """
        mob.on_move(
            action=Action.MOVE_LEFT,
            slot=lambda obj, parent=self: parent._move_object(obj, -1, 0),
        )
        mob.on_move(
            action=Action.MOVE_RIGHT,
            slot=lambda obj, parent=self: parent._move_object(obj, 1, 0),
        )
        mob.on_move(
            action=Action.MOVE_UP,
            slot=lambda obj, parent=self: parent._move_object(obj, 0, -1),
        )
        mob.on_move(
            action=Action.MOVE_DOWN,
            slot=lambda obj, parent=self: parent._move_object(obj, 0, 1),
        )

    def _create_ghost(
        self, initial_state: State, type: GhostType, action: Action
    ) -> Ghost:
        """Helper method for instantiating ghost and assigning default
        movement callbacks to it.

        Parameters
        ----------
        initial_state : State
        type : GhostType
        action : Action

        Returns
        -------
        Ghost
            Mob with default movement callbacks already assigned.
        """
        ghost = Ghost.create(state=initial_state, ghost_type=type, action=action)
        self._initialize_movement_callbacks(mob=ghost)
        self.ghosts.append(ghost)
        return ghost

    def _create_packman(self, initial_state: State, action: Action) -> Pacman:
        """Helper method for instantiating pacman and assigning default
        movement callbacks to it.

        Parameters
        ----------
        initial_state : State
            Initial state of the mob.
        action : Action
            Initial action of the mob.

        Returns
        -------
        Pacman
            Mob with default movement callbacks already assigned.
        """
        pacman = Pacman(state=initial_state, action=action)
        self._initialize_movement_callbacks(pacman)
        pacman.on_collision(Coin, lambda other: self.consume_coin(coin=other))
        pacman.on_collision(Ghost, lambda _: self.setHearts(self.hearts - 1))
        self.pacman = pacman
        return pacman

    def _unravel_weight(self, layout: np.ndarray, x: int, y: int) -> list[Animated]:
        """Unravels weight of a specific cell into a list of objects
        placed there.

        Parameters
        ----------
        layout : np.ndarray
            A numeric representation of a map.
        x : int
            A column position of a cell needs to be unraveled.
        y : int
            A row position of a cell needs to be unraveled.

        Returns
        -------
        list[Animated]
            A list of objects from the cell.
        """
        if layout[y, x] == 1:
            return [Wall.create(wall_type=WallType.infer(layout=layout, x=x, y=y))]

        result = [Floor()]
        weight = layout[y, x]
        ghost_types = deque(GhostType._member_map_.values())
        while weight > 0:
            if weight - EntityWeight.GHOST_WEIGHT >= 0:
                result.append(
                    self._create_ghost(
                        initial_state=State(pos_x=x, pos_y=y),
                        type=ghost_types.pop(),
                        action=Action.MOVE_UP,
                    )
                )
                weight -= EntityWeight.GHOST_WEIGHT
            elif weight - EntityWeight.PACMAN_WEIGHT >= 0:
                result.append(
                    self._create_packman(
                        initial_state=State(pos_x=x, pos_y=y), action=Action.MOVE_UP
                    )
                )
                weight -= EntityWeight.PACMAN_WEIGHT
            elif weight - EntityWeight.COIN_WEIGHT >= 0:
                result.append(Coin(state=State(pos_x=x, pos_y=y)))
                weight -= EntityWeight.COIN_WEIGHT
        return result

    def _layout_from_map(self, layout: np.ndarray) -> list[Tile]:
        """Generates an object-oriented representation of a populated
        maze from numeric representation into a 1d array of tiles.

        Parameters
        ----------
        layout : np.ndarray
            A numeric representation of a maze.

        Returns
        -------
        list[Tile]
            A 1d array of tiles.
        """
        result = [None] * layout.size

        for row_index, row in enumerate(layout):
            for column_index, _ in enumerate(row):
                result[row_index * self.ncols + column_index] = Tile(
                    objects=self._unravel_weight(
                        layout=layout, x=column_index, y=row_index
                    )
                )

        return result

    def tile(self, x: int, y: int) -> Tile:
        """A getter method to look into a specific tile
        on the map.

        Parameters
        ----------
        x : int
            Column where the tile is placed.
        y : int
            Row where the tile is placed.

        Returns
        -------
        Tile
            Tile in the position (x, y).
        """
        if y < 0 or y >= self.nrows:
            raise ValueError(
                f"Y coordinate is out of range: "
                f"provided {y}, max_y_value {self.nrows - 1}"
            )
        if x < 0 or x >= self.ncols:
            raise ValueError(
                f"X coordinate is out of range: "
                f"provided {x}, max_x_value {self.ncols - 1}"
            )

        return self.tiles[y * self.ncols + x]

    def state(self) -> MazeState:
        """Generates state object for the maze."""
        return MazeState(
            ghost_states=[ghost.current_state for ghost in self.ghosts],
            pacman_state=self.pacman.current_state,
            score=self.score,
            hearts=self.hearts,
        )
