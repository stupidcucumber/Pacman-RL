from collections import deque
from dataclasses import dataclass
from typing import Callable

import numpy as np
from packmanvis.algorithms.maze import generate_pacmanlike_maze
from packmanvis.algorithms.maze.types import EntityWeight
from packmanvis.types.action import Action
from packmanvis.types.entity import Entity
from packmanvis.types.items import Coin
from packmanvis.types.mobs import Ghost, GhostType, Mob, Pacman
from packmanvis.types.state import State

from .animated import Animated
from .structure import Floor, Wall, WallType


@dataclass
class Tile:
    objects: list[Animated]

    @property
    def is_wall(self) -> bool:
        return isinstance(self.objects[0], Wall)

    def pop(self, obj: Animated) -> None:
        self.objects.remove(obj)

    def append(self, obj: Animated) -> bool:
        if self.is_wall:
            return False
        self.objects.append(obj)
        return True


class Maze:
    def __init__(self, shape: tuple[int, int]) -> None:
        self.layout = generate_pacmanlike_maze(shape=shape)
        self.nrows = self.layout.shape[0]
        self.ncols = self.layout.shape[1]
        self.tiles: list[Tile] = self._layout_from_map(self.layout)

        self.on_score_changed_slot: Callable[[], None] | None = None

        self.score: int = 0
        self.hearts: int = 3

    def setScore(self, score: int) -> None:
        self.score = score
        self.on_score_changed_slot()

    def destroy(self, obj: Entity) -> None:
        self.tile(obj.current_state.pos_x, obj.current_state.pos_y).pop(obj)
        obj.destroy()

    def consume_coin(self, coin: Coin) -> None:
        self.setScore(self.score + 50)
        self.destroy(coin)

    def on_score_changed(self, slot: Callable[[], None]) -> None:
        self.on_score_changed_slot = slot

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
            return True
        return False

    def _initialize_movement_callbacks(self, mob: Mob) -> None:
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
        ghost = Ghost.create(state=initial_state, ghost_type=type, action=action)
        self._initialize_movement_callbacks(mob=ghost)
        return ghost

    def _create_packman(self, initial_state: State, action: Action) -> Pacman:
        pacman = Pacman(state=initial_state, action=action)
        self._initialize_movement_callbacks(pacman)
        pacman.on_collision(Coin, lambda other: self.consume_coin(coin=other))
        pacman.on_collision(Ghost, lambda other: ...)
        return pacman

    def _create_coin(self, initial_state: State) -> Coin:
        coin = Coin(state=initial_state, action=Action.STAY)
        coin.on_collision(Pacman, lambda other: self.destroy(coin))
        return coin

    def _unravel_weight(self, layout: np.ndarray, x: int, y: int) -> list[Animated]:
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
                result.append(self._create_coin(initial_state=State(pos_x=x, pos_y=y)))
                weight -= EntityWeight.COIN_WEIGHT
        return result

    def _layout_from_map(self, layout: np.ndarray) -> list[Tile]:
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
