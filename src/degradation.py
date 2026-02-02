import numpy as np

class TyreDegradationModel:
    def __init__(self, alpha=0.03):
        self.alpha = alpha

    def fit(self, data):
        self.tyre_life = data["tyre_life"].values
        return self

    def predict(self, tyre_life):
        return np.exp(-self.alpha * tyre_life)