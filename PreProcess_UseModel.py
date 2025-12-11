# PreProcess_UseModel.py
"""
Module that combines preprocessing + model prediction in one step.
It is called by main.py or LLM_G.

Pipeline:
1. Receive raw or structured sensor input
2. Apply preprocessing rules
3. Select ML model based on machine or ontology hints
4. Run prediction
5. Produce a standardized prediction dictionary
"""

from typing import Dict, Any
from SensorInput import sensor_input
from model_select import model_selector


class PreProcessUseModel:
    def __init__(self):
        pass

    def run(self, sensor_json: Dict[str, Any], model_name: str = "random_forest") -> Dict[str, Any]:
        """
        Full mini-pipeline for model inference.
        Returns a prediction dictionary that LLM_G or OntologyAccess
        can consume.
        """

        # 1. Parse
        parsed = sensor_input.parse(sensor_json)

        # 2. Validate
        if not sensor_input.validate(parsed):
            return {"error": "invalid_sensor_input"}

        # 3. Preprocess
        processed = sensor_input.preprocess(parsed)

        # 4. Model selection + prediction
        prediction = model_selector.predict(model_name, processed)

        # 5. Build standardized response
        result = {
            "machine_id": parsed["machine_id"],
            "raw": parsed,
            "processed": processed,
            "model_used": model_name,
            "prediction": prediction,
        }

        return result


# Global instance
PreProcessor = PreProcessUseModel()
