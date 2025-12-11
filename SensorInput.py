# SensorInput.py
"""
Module responsible for reading, validating and structuring sensor inputs
before sending them to predictive models or the LLM manager.

This is a placeholder version until actual sensor fields are provided.
"""

from typing import Dict, Any

class SensorInput:
    def __init__(self):
        pass

    def parse(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert raw sensor JSON/input into a normalized structure.
        Example expected fields (can be updated later):
            - machine_id
            - temperature
            - vibration
            - pressure
            - noise
        """
        structured = {
            "machine_id": raw_input.get("machine_id", "UNKNOWN"),
            "temperature": float(raw_input.get("temperature", 0.0)),
            "vibration": float(raw_input.get("vibration", 0.0)),
            "pressure": float(raw_input.get("pressure", 0.0)),
            "noise": float(raw_input.get("noise", 0.0)),
        }
        return structured

    def validate(self, data: Dict[str, Any]) -> bool:
        """
        Basic validation for missing or impossible values.
        Expand later based on domain needs.
        """
        if data["machine_id"] == "UNKNOWN":
            return False
        return True

    def preprocess(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess values before sending to ML models.
        Placeholder for scaling, normalization etc.
        """
        # Example normalization placeholder
        data["temperature_norm"] = data["temperature"] / 100.0
        data["vibration_norm"] = data["vibration"] / 10.0
        return data

sensor_input = SensorInput()
