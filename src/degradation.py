import numpy as np

class TyreDegradationModel:
    def __init__(self, alpha=0.02):
        self.alpha = alpha

    def fit(self, data):
        return self

    def predict(self, stint_length):
        laps = np.arange(stint_length)
        return np.exp(-self.alpha * laps)