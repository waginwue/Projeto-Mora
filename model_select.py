# model_select.py

"""
Module for selecting which predictive model to use (CNN, LSTM, or Random Forest).
This version loads the models from models/ and exposes a simple function
`select_model` that your LLM_G or FastAPI route can call.
"""

from models.CNN import CNNModel
from models.LSTM import LSTMModel
from models.randon_forest import RandomForestModel

class ModelSelector:
    def __init__(self):
        # Instantiate all models (or lazily load depending on your structure)
        self.models = {
            "cnn": CNNModel(),
            "lstm": LSTMModel(),
            "random_forest": RandomForestModel(),
        }

    def list_models(self):
        """Return available model names."""
        return list(self.models.keys())

    def select_model(self, model_name: str):
        """
        Return a model instance by name.
        If name not found, return default model (e.g., random_forest).
        """
        model_name = model_name.lower()
        return self.models.get(model_name, self.models["random_forest"])

    def predict(self, model_name: str, data):
        """
        Call predict() from selected model.
        """
        model = self.select_model(model_name)
        return model.predict(data)

# If you want a global instance
model_selector = ModelSelector()
