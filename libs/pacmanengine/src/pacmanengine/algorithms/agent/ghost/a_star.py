from heapq import heappop, heappush

import numpy as np


def manhattan_distance(point_A: tuple[int, int], point_B: tuple[int, int]) -> int:
    """Calculates Manhattan distance from the point_A to the point_B.

    Parameters
    ----------
    point_A, point_B : tuple[int, int]
        Points between which to calculate the distance.

    Returns
    -------
    int
        Distance.
    """
    return abs(point_A[0] - point_B[0]) + abs(point_A[1] - point_B[1])


def a_star(
    start: tuple[int, int], goal: tuple[int, int], grid: np.ndarray
) -> list[tuple[int, int]] | None:
    """
    A* algorithm to find the shortest path in a 2D grid with obstacles.

    Parameters
    ----------
    start : tuple[int, int]
        Start point in the format (y, x).
    goal : tuple[int, int]
        Point where you want to go in the format (y, x).
    grid : np.ndarray
        Layout of the maze, where 1 is a wall.

    Returns
    -------
    list[tuple[int, int]] | None
        The shortest path from start to goal (as a list of points),
        or None if no path exists. Points are in the format (y, x).
    """
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    rows = len(grid)
    cols = len(grid[0])
    open_set = []
    heappush(open_set, (0, start))
    g_score = {start: 0}
    came_from = {}
    visited = set()

    while open_set:
        _, current = heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        visited.add(current)
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if (
                0 <= neighbor[0] < rows
                and 0 <= neighbor[1] < cols
                and grid[neighbor[0]][neighbor[1]] != 1
                and neighbor not in visited
            ):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_cost = tentative_g_score + manhattan_distance(neighbor, goal)
                    heappush(open_set, (f_cost, neighbor))

    return None


def reconstruct_path(
    came_from: dict, current: tuple[int, int]
) -> list[tuple[int, int]]:
    """
    Reconstruct the path from start to goal.

    Parameters
    ----------
    came_from : dict
        A dictionary with the backtrace from each point to the previous point.
    current : tuple[int, int]
        The current point (goal) to start backtracking from.

    Returns
    -------
    list
        The shortest path as a list of points.
    """
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]  # Reverse the path to get it from start to goal
