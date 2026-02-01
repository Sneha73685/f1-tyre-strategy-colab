import numpy as np

def simulate_strategy(degradation_model, total_laps, pit_window):
    strategy_cost = []

    for pit_lap in range(pit_window[0], pit_window[1]):
        tyre_life_stint1 = np.arange(1, pit_lap + 1)
        tyre_life_stint2 = np.arange(1, total_laps - pit_lap + 1)

        stint1 = degradation_model.predict(tyre_life_stint1)
        stint2 = degradation_model.predict(tyre_life_stint2)

        cost = np.sum(stint1) + np.sum(stint2)
        strategy_cost.append((pit_lap, cost))

    return strategy_cost