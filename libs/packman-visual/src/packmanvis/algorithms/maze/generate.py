import numpy as np
from mazelib.generate.AldousBroder import AldousBroder


def generate_maze(shape: tuple[int, int]) -> np.ndarray:
    """Generates maze following AldousBroder algorithm.

    Parameters
    ----------
    shape : tuple[int, int]
        Shape of the desired maze in the form of (H, W).

    Returns
    -------
    np.ndarray
    """
    generator = AldousBroder(*shape)
    return generator.generate()
