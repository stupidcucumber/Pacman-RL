from __future__ import annotations

from collections import deque
from dataclasses import dataclass

import numpy as np


@dataclass
class BacktrackItem:
    """Support class for storing additional info
    about item in the backtracking stack.

    Attributes
    ----------
    previous_position : tuple[int, int]
        Previous wall tile position in the
        format (Y, X).
    current_position : tuple[int, int]
        Current wall tile position in the
        format (Y, X).
    length : int
        Length of a wall up to this point.
    """

    previous_position: tuple[int, int]
    current_position: tuple[int, int]
    length: int


def _populate_backtrack_stack(
    stack: deque,
    previous_position: tuple[int, int],
    next_positions: list[tuple[int, int]],
    length: int,
) -> None:
    """Pushes all found next positions to the backtrack stack.

    Parameters
    ----------
    stack : deque
        Stack object that needs to be populated.
    previous_position : tuple[int, int]
        Previous position in format (Y, X).
    next_positions : list[tuple[int, int]]
        A list of next positions in format (Y, X).
    length : int
        Length of the wall up to the next position.
    """
    for next_position in next_positions:
        if next_position != previous_position:
            stack.append(
                BacktrackItem(
                    previous_position=previous_position,
                    current_position=next_position,
                    length=length,
                )
            )


def _find_available_paths(
    maze: np.ndarray, position: tuple[int, int], exclude: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    """Finds available cellso to move on from the current postion.

    Parameters
    ----------
    maze : np.ndarray
        Maze represented as a np.ndarray, where 1 mean wall, and 0
        means path.
    position : tuple[int, int]
        The (Y, X) of the current position.
    exclude : list[tuple[int, int]]
        Positions that needs to be excluded from the result set.

    Returns
    -------
    list[tuple[int, int]]
        List of probable positions where one can move to
        in the form of (Y, X) tuples.
    """
    paths = []
    if position[0] > 0 and maze[position[0] - 1, position[1]]:
        paths.append((position[0] - 1, position[1]))
    if position[0] < maze.shape[0] - 1 and maze[position[0] + 1, position[1]]:
        paths.append((position[0] + 1, position[1]))
    if position[1] > 0 and maze[position[0], position[1] - 1]:
        paths.append((position[0], position[1] - 1))
    if position[1] < maze.shape[1] - 1 and maze[position[0], position[1] + 1]:
        paths.append((position[0], position[1] + 1))
    return [path for path in paths if path not in exclude]


def _find_branch_roots(maze: np.ndarray) -> list[BacktrackItem]:
    """Finds roots of the banch.

    Parameters
    ----------
    maze : np.ndarray
        Numpy representation of maze.

    Returns
    -------
    list[BacktrackItem]
        List of BacktrackItem values representing roots of the
        branches.

    Notes
    -----
    Searching for the bases of branches near border.
    We can do so beacause all walls in the maze are rooted
    to the border walls of the map. Also none of the walls
    are intersect each other, because otherwise we would have
    had a closed sections.
    """
    roots = []

    for x_coord, value in enumerate(maze[1]):
        if value == 1 and x_coord not in [0, maze.shape[1] - 1]:
            roots.append(
                BacktrackItem(
                    previous_position=(0, x_coord),
                    current_position=(1, x_coord),
                    length=1,
                )
            )

    for x_coord, value in enumerate(maze[-2]):
        if value == 1 and x_coord not in [0, maze.shape[1] - 1]:
            roots.append(
                BacktrackItem(
                    previous_position=(maze.shape[0] - 1, x_coord),
                    current_position=(maze.shape[0] - 2, x_coord),
                    length=1,
                )
            )

    for y_coord, value in enumerate(maze[:, 1]):
        if value == 1 and y_coord not in [0, maze.shape[0] - 1]:
            roots.append(
                BacktrackItem(
                    previous_position=(y_coord, 0),
                    current_position=(y_coord, 1),
                    length=1,
                )
            )

    for y_coord, value in enumerate(maze[:, -2]):
        if value == 1 and y_coord not in [0, maze.shape[0] - 1]:
            roots.append(
                BacktrackItem(
                    previous_position=(y_coord, maze.shape[1] - 1),
                    current_position=(y_coord, maze.shape[1] - 2),
                    length=1,
                )
            )

    return roots


def _stratificate_branch(
    maze: np.ndarray,
    root: BacktrackItem,
    min_len: int = 3,
    max_len: int = 6,
    threshold: float = 0.5,
) -> list[tuple[int, int]]:
    """Finds indeces of the elements that can be zeroed to avoid long walls.
    - If wall length is between `min_len` and `max_len`, then it
    puts hole with a 0.5 chance.
    - If wall length is more than `max_len`, then it puts hole with a
    1.0 chance.

    Parameters
    ----------
    maze : np.ndarray
        Maze representation.
    root : BacktrackItem
        The BacktrackItem of the branch root.
    min_len : int, default=3
        Minimum length of the wall.
    max_len : int, default=6
        Maximum length of the wall.
    threshold : float, default=0.5
        Chance that the length between `min_len` and `max_len`
        will be stratified.

    Returns
    -------
    list[tuple[int, int]]
        Indeces of an element in a maze that needs to be equal to zero
        for maze to have less dead ends in the form of (Y, X) tuples.
    """
    backtrack_stack: deque[BacktrackItem] = deque()
    backtrack_stack.append(root)
    zeroing_indeces = []

    while len(backtrack_stack) != 0:
        backtrack_item = backtrack_stack.pop()
        length = backtrack_item.length
        if length > min_len and length <= max_len:
            if np.random.randn() < threshold:
                zeroing_indeces.append(backtrack_item.current_position)
                length = 0
        elif length > max_len:
            zeroing_indeces.append(backtrack_item.current_position)
            length = 0

        length += 1
        available_paths = _find_available_paths(
            maze,
            backtrack_item.current_position,
            exclude=[backtrack_item.previous_position],
        )
        _populate_backtrack_stack(
            backtrack_stack, backtrack_item.current_position, available_paths, length
        )

    return zeroing_indeces


def strave_maze(maze: np.ndarray) -> np.ndarray:
    """Makes holes in the maze to avoid dead ends.

    Parameters
    ----------
    maze : np.ndarray
        Maze representation where element 1 means
        wall, and element 0 means path.

    Returns
    -------
    np.ndarray
        Maze with holes inside the walls.
    """
    zeroing_indeces = []
    roots = _find_branch_roots(maze)
    for root in roots:
        zeroing_indeces.extend(_stratificate_branch(maze, root, threshold=0.3))
    for y, x in zeroing_indeces:
        maze[y, x] = 0
    return maze
