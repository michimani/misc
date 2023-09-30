import numpy as np


def distance(a: np.ndarray, b: np.ndarray) -> np.floating:
    return np.linalg.norm(a - b)
