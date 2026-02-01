import numpy as np

class TyreDegradationModel:
    def __init__(self, alpha=0.03):
        self.alpha = alpha

    def fit(self, data):
        self.laps = data["lap"].values
        return self

    def predict(self):
        return np.exp(-self.alpha * self.laps)