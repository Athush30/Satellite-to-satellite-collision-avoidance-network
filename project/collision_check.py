import numpy as np

def check_collision(pos1, pos2, threshold_km=10):
    distance = np.linalg.norm(pos1 - pos2)
    return distance < threshold_km, distance
