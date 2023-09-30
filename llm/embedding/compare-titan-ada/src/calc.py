import numpy as np


def distance(a: np.ndarray, b: np.ndarray) -> np.floating:
    return np.linalg.norm(a - b)


def similarity(a: np.ndarray, b: np.ndarray) -> np.floating:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
