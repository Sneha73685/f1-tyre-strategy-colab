import numpy as np

class TyreDegradationModel:
    def __init__(self, compound="Medium"):
        self.compound = compound
        self.alpha_map = {
            "Soft": 0.045,
            "Medium": 0.030,
            "Hard": 0.020
        }
        self.alpha = self.alpha_map[compound]

    def fit(self, data):
        return self

    def predict(self, tyre_life):
        return np.exp(-self.alpha * tyre_life)