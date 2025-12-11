#Formularios com texto entram aqui e são processados, para os dados serem armazenados na Ontologia ou banco de dados
# FORM_TEXT_INPUT.py
"""
Module for handling free-text or mixed-form inputs.
This acts as an intermediate layer between user/operator inputs
and the LLM manager.
"""

from typing import Dict

class FormTextInput:
    def __init__(self):
        pass

    def parse(self, text: str) -> Dict:
        """
        Basic parser that converts natural-language or semi-structured text
        into preliminary structured fields.

        Example:
            "M2 vibração alta e ruído médio"
        """

        normalized = text.lower()

        machine = None
        if "m1" in normalized:
            machine = "M1"
        elif "m2" in normalized:
            machine = "M2"
        elif "m3" in normalized:
            machine = "M3"

        # Placeholder extraction rules
        data = {
            "machine": machine,
            "raw_text": text
        }

        return data

    def enrich_with_default_sensors(self, parsed: Dict) -> Dict:
        """
        If operator only sends text, we can fill missing fields
        with default sensor values or leave them None.
        """
        parsed.setdefault("temperature", None)
        parsed.setdefault("vibration", None)
        parsed.setdefault("pressure", None)
        parsed.setdefault("noise", None)
        return parsed

form_text_input = FormTextInput()
