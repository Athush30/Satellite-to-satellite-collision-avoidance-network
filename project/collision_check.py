import numpy as np

def check_collision(pos1, pos2, sat1_name, sat2_name, threshold_km=10):
    """
    Check if two satellites are at risk of collision based on distance.
    Args:
        pos1: Position of satellite 1 (km, numpy array)
        pos2: Position of satellite 2 (km, numpy array)
        sat1_name: Name of satellite 1
        sat2_name: Name of satellite 2
        threshold_km: Collision risk threshold (km, default 10)
    Returns:
        tuple: (risk, distance) where risk is True if distance < threshold_km and valid
    """
    distance = np.linalg.norm(pos1 - pos2)
    # Handle zero or near-zero distances (possible TLE error)
    if distance < 0.001:  # Less than 1 meter
        print(f"Warning: Unrealistic distance {distance:.2f} km between {sat1_name} and {sat2_name}. Check TLE data.")
        return False, distance
    risk = distance < threshold_km
    print(f"Collision check between {sat1_name} and {sat2_name}: Distance = {distance:.2f} km, Risk = {risk}")
    return risk, distance
