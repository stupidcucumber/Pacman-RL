from __future__ import annotations
from packmanvis.types.mobs import Mob
from packmanvis.types.wall import Wall, WallType
import numpy as np


class Labirinth:
    def __init__(self, walls_layout: np.ndarray | None = None) -> None:
        self.map = Labirinth._map_from_layout(walls_layout)

    @staticmethod
    def _generate_walls_lower_left_corner(shape: tuple[int, int]) -> np.ndarray:
        layout = np.zeros(shape=shape)
        layout[:, 0] = 1
        layout[-1] = 1 
        return layout

    @staticmethod
    def _generate_walls_layout_from_corner(ll_corner: np.ndarray) -> np.ndarray:
        ul_corner = np.flipud(ll_corner)
        lr_corner = np.fliplr(ll_corner)
        ur_corner = np.fliplr(ul_corner)
        upper_map = np.hstack((ul_corner, ur_corner))
        lower_map = np.hstack((ll_corner, lr_corner))
        return np.vstack(
            [
                upper_map, 
                lower_map
            ]
        )

    @staticmethod
    def _generate_walls_center(layout: np.ndarray) -> np.ndarray:
        y_center = layout.shape[0] // 2
        x_center = layout.shape[1] // 2
        layout[[y_center, y_center + 1], x_center:x_center+1] = 1 # FOR TEST IT IS 1
        return layout
    
    @staticmethod
    def _map_from_layout(layout: np.ndarray) -> list:
        result = []
        for y in layout:
            row = []
            for x in y:
                row.append(
                    Wall(type=WallType.VERTICAL_OPENED) if x == 1 else []
                )
            result.append(row)
        return result
    
    @staticmethod
    def _populate_labirinth(layout: np.ndarray, mobs: list[Mob]) -> np.ndarray:
        pass
    
    @classmethod
    def generate(cls, seed: int = 42) -> Labirinth:
        corner = cls._generate_walls_lower_left_corner(shape=(10, 20))
        raw_layout = cls._generate_walls_layout_from_corner(ll_corner=corner)
        walls_layout = cls._generate_walls_center(raw_layout)
        return Labirinth(walls_layout=walls_layout)
        
    def reset(self, mobs: list[Mob]) -> None:
        pass 
    
    def update(self, mobs: list[Mob]) -> ...:
        pass
