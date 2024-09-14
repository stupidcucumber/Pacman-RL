from __future__ import annotations

import enum

import numpy as np

PREFIX = "wall_sprite"


class WallType(enum.StrEnum):
    """Enum class responsible for mapping
    sprite of the wall to the Wall object.

    Attributes
    ----------
    VERTICAL_OPENED : str
        Type of the tile where there are openings only to the
        down and up direction:
        ```
            +---------+
            |   OOO   |
            |   OOO   |
            |   OOO   |
            +---------+
        ```
    HORIZONTAL_OPENED: str
        Type of the tile where there are openings only to the
        left and right direction:
        ```
            +---------+
            |         |
            |OOOOOOOOO|
            |         |
            +---------+
        ```
    CROSS: str
        Type of the tile where there are openings to all directions,
        meaning left, up, down and right:
        ```
            +---------+
            |   OOO   |
            |OOOOOOOOO|
            |   OOO   |
            +---------+
        ```
    LEFT_T: str
        Type of the tile where there are openings to the left, up and
        down:
        ```
            +---------+
            |   OOO   |
            |OOOOOO   |
            |   OOO   |
            +---------+
        ```
    T: str
        Type of the tile where there are openings to the down, left and
        right directions:
        ```
            +---------+
            |         |
            |OOOOOOOOO|
            |   OOO   |
            +---------+
        ```
    RIGHT_T: str
        Type of the tile where there are opening to the up, down and right
        directions:
        ```
            +---------+
            |   OOO   |
            |   OOOOOO|
            |   OOO   |
            +---------+
        ```
    UPSIDE_DOWN_T: str
        Type of the Tile where there are opening to the up, right and left
        directions:
        ```
            +---------+
            |   OOO   |
            |OOOOOOOOO|
            |         |
            +---------+
        ```
    DL_CORNER: str
        Type of the Tile where there are openings only to the up and left:
    DR_CORNER: str
    UR_CORNER: str
    UL_CORNER: str
    HORIZONTAL_LEFT_CLOSED: str
    VERTICAL_UP_CLOSED: str
    HORIZONTAL_RIGHT_CLOSED: str
    VERTICAL_DOWN_CLOSED: str
    """

    VERTICAL_OPENED: str = f"{PREFIX}:0.png"
    HORIZONTAL_OPENED: str = f"{PREFIX}:1.png"
    CROSS: str = f"{PREFIX}:2.png"
    LEFT_T: str = f"{PREFIX}:3.png"
    T: str = f"{PREFIX}:4.png"
    RIGHT_T: str = f"{PREFIX}:5.png"
    UPSIDE_DOWN_T: str = f"{PREFIX}:6.png"
    DL_CORNER: str = f"{PREFIX}:7.png"
    DR_CORNER: str = f"{PREFIX}:8.png"
    UR_CORNER: str = f"{PREFIX}:9.png"
    UL_CORNER: str = f"{PREFIX}:10.png"
    HORIZONTAL_LEFT_CLOSED: str = f"{PREFIX}:11.png"
    VERTICAL_UP_CLOSED: str = f"{PREFIX}:12.png"
    HORIZONTAL_RIGHT_CLOSED: str = f"{PREFIX}:13.png"
    VERTICAL_DOWN_CLOSED: str = f"{PREFIX}:14.png"

    @staticmethod
    def _x_on_right_border(layout: np.ndarray, x: int) -> bool:
        """Checks whether the X coordinate is resides on the
        right border of the Labirinth.

        Parameters
        ----------
        layout : np.ndarray
            Layout of the Labirinth.
        x : int
            X coordinate.

        Returns
        -------
        bool
            True if x lies on the right border of the map.
        """
        return x == layout.shape[1] - 1

    @staticmethod
    def _y_on_down_border(layout: np.ndarray, y: int) -> bool:
        """Checks whether the Y coordinate is resides on the
        down border of the Labirinth.

        Parameters
        ----------
        layout : np.ndarray
            Layout of the Labirinth.
        y : int
            Y coordinate.

        Returns
        -------
        bool
            True if y lies on the down border of the map.
        """
        return y == layout.shape[0] - 1

    @staticmethod
    def _infer_wall_type_CROSS(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any(
            [
                x == 0,
                y == 0,
                WallType._x_on_right_border(layout, x),
                WallType._y_on_down_border(layout, y),
            ]
        ):
            return False, None, 0
        return (
            all(
                [layout[y - 1, x], layout[y + 1, x], layout[y, x - 1], layout[y, x + 1]]
            ),
            WallType.CROSS,
            14,
        )

    @staticmethod
    def _infer_wall_type_T(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any(
            [
                x == 0,
                WallType._x_on_right_border(layout, x),
                WallType._y_on_down_border(layout, y),
            ]
        ):
            return False, None, 0
        return (
            all([layout[y, x - 1], layout[y, x + 1], layout[y + 1, x]]),
            WallType.T,
            13,
        )

    @staticmethod
    def _infer_wall_type_UPSIDE_DOWN_T(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any([y == 0, x == 0, WallType._x_on_right_border(layout, x)]):
            return False, None, 0
        return (
            all([layout[y, x - 1], layout[y, x + 1], layout[y - 1, x]]),
            WallType.UPSIDE_DOWN_T,
            13,
        )

    @staticmethod
    def _infer_wall_type_LEFT_T(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any([x == 0, y == 0, WallType._y_on_down_border(layout, y)]):
            return False, None, 0
        return (
            all([layout[y - 1, x], layout[y + 1, x], layout[y, x - 1]]),
            WallType.LEFT_T,
            13,
        )

    @staticmethod
    def _infer_wall_type_RIGHT_T(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any(
            [
                y == 0,
                WallType._x_on_right_border(layout, x),
                WallType._y_on_down_border(layout, y),
            ]
        ):
            return False, None, 0
        return (
            all([layout[y - 1, x], layout[y + 1, x], layout[y, x + 1]]),
            WallType.RIGHT_T,
            13,
        )

    @staticmethod
    def _infer_wall_type_DL_CORNER(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any([y == 0, WallType._x_on_right_border(layout, x)]):
            return False, None, 0
        return all([layout[y - 1, x], layout[y, x + 1]]), WallType.DL_CORNER, 12

    @staticmethod
    def _infer_wall_type_DR_CORNER(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any([y == 0, x == 0]):
            return False, None, 0
        return all([layout[y - 1, x], layout[y, x - 1]]), WallType.DR_CORNER, 12

    @staticmethod
    def _infer_wall_type_UR_CORNER(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any([WallType._y_on_down_border(layout, y), x == 0]):
            return False, None, 0
        return all([layout[y + 1, x], layout[y, x - 1]]), WallType.UR_CORNER, 12

    @staticmethod
    def _infer_wall_type_UL_CORNER(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any(
            [
                WallType._y_on_down_border(layout, y),
                WallType._x_on_right_border(layout, x),
            ]
        ):
            return False, None, 0
        return all([layout[y + 1, x], layout[y, x + 1]]), WallType.UL_CORNER, 12

    @staticmethod
    def _infer_wall_type_HORIZONTAL_OPENED(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any([x == 0, WallType._x_on_right_border(layout, x)]):
            return False, None, 0
        return all([layout[y, x - 1], layout[y, x + 1]]), WallType.HORIZONTAL_OPENED, 11

    @staticmethod
    def _infer_wall_type_VERTICAL_OPENED(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any([y == 0, WallType._y_on_down_border(layout, y)]):
            return False, None, 0
        return all([layout[y - 1, x], layout[y + 1, x]]), WallType.VERTICAL_OPENED, 11

    @staticmethod
    def _infer_wall_type_HORIZONTAL_LEFT_CLOSED(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any([WallType._x_on_right_border(layout, x)]):
            return False, None, 0
        return all([layout[y, x + 1]]), WallType.HORIZONTAL_LEFT_CLOSED, 10

    @staticmethod
    def _infer_wall_type_HORIZONTAL_RIGHT_CLOSED(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any([x == 0]):
            return False, None, 0
        return all([layout[y, x - 1]]), WallType.HORIZONTAL_RIGHT_CLOSED, 10

    @staticmethod
    def _infer_wall_type_VERTICAL_UP_CLOSED(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any([WallType._y_on_down_border(layout, y)]):
            return False, None, 0
        return all([layout[y + 1, x]]), WallType.HORIZONTAL_RIGHT_CLOSED, 10

    @staticmethod
    def _infer_wall_type_VERTICAL_DOWN_CLOSED(
        layout: np.ndarray, x: int, y: int
    ) -> tuple[bool, WallType, int]:
        if any([y == 0]):
            return False, None, 0
        return all([layout[y - 1, x]]), WallType.HORIZONTAL_LEFT_CLOSED, 10

    @staticmethod
    def infer(layout: np.ndarray, x: int, y: int) -> WallType:
        """Infers the type of the wall from the passed layout and
        coordinates of the current tile.

        Parameters
        ----------
        layout : np.ndarray
            Layout containing 1 for the wall tile, and 0 for the
            non-wall tile.
        x : int
            X coordinate of the Tile.
        y : int
            Y coordinate of the Tile.

        Returns
        -------
        WallType
            Type of the wall that lays on the postion (x, y).
        """
        infer_methods = [
            name for name in WallType.__dict__.keys() if name.startswith("_infer")
        ]
        result_type: WallType = WallType.VERTICAL_DOWN_CLOSED
        highest_weight: int = 0
        for infer_method in infer_methods:
            accepted, wall_type, type_weight = WallType.__dict__[infer_method](
                layout, x, y
            )
            if accepted and type_weight > highest_weight:
                highest_weight = type_weight
                result_type = wall_type
        return result_type