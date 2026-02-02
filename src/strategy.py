import numpy as np

def compute_stint_cost(model, stint_length):
    tyre_life = np.arange(1, stint_length + 1)
    performance = model.predict(tyre_life)
    degradation_cost = np.sum(1 - performance)
    return degradation_cost


def one_stop_strategy(model, total_laps, pit_lap):
    stint1 = compute_stint_cost(model, pit_lap)
    stint2 = compute_stint_cost(model, total_laps - pit_lap)
    return stint1 + stint2


def two_stop_strategy(model, total_laps, pit1, pit2):
    stint1 = compute_stint_cost(model, pit1)
    stint2 = compute_stint_cost(model, pit2 - pit1)
    stint3 = compute_stint_cost(model, total_laps - pit2)
    return stint1 + stint2 + stint3