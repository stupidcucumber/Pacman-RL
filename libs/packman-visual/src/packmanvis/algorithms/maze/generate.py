import numpy as np
from mazelib.generate.AldousBroder import AldousBroder
from packmanvis.algorithms.maze.strave import strave_maze


def generate_maze(shape: tuple[int, int]) -> np.ndarray:
    """Generates maze following AldousBroder algorithm.

    Parameters
    ----------
    shape : tuple[int, int]
        Shape of the desired maze in the form of (H, W).

    Returns
    -------
    np.ndarray
        Maze representation.
    """
    generator = AldousBroder(*shape)
    return generator.generate()


def generate_straved_maze(shape: tuple[int, int]) -> np.ndarray:
    """Generates straved maze.

    Parameters
    ----------
    shape : tuple[int, int]
        Shape of the desired maze in the form of (H, W).

    Returns
    -------
    np.ndarray
        Maze with little to no dead ends.
    """
    maze = generate_maze(shape)
    return strave_maze(maze)


def _put_ghost_home(maze: np.ndarray) -> np.ndarray:
    """Puts a ghost home at the center of a maze.

    Parameters
    ----------
    maze : np.ndarray
        A pacman-like representation of a maze.

    Returns
    -------
    np.ndarray
        Maze with home for ghosts in the middle.
    """
    center_y, center_x = [value // 2 for value in maze.shape[:2]]

    maze[center_y - 1 : center_y + 4, center_x - 3 : center_x + 2] = 0
    maze[center_y : center_y + 3, center_x - 2 : center_x + 1] = 1
    maze[center_y : center_y + 2, center_x - 1 : center_x] = 0

    return maze


def generate_pacmanlike_maze(shape: tuple[int, int]) -> np.ndarray:
    """Generates a maze that looks like a maze in pacman.
    Therefore it has little to no dead ends and most of
    paths are one tile wide.


    Parameters
    ----------
    shape : tuple[int, int]
        Shape of the desired maze in the form of (H, W).

    Returns
    -------
    np.ndarray
        Pacman maze representation.
    """
    straved_maze = generate_straved_maze(shape=shape)
    return _put_ghost_home(straved_maze)
