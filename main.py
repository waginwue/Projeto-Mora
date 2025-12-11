# main.py
"""
Main entry point of Projeto-Mora.
This connects:
- SensorInput
- ModelSelector
- OntologyAccess
- LLM_G (manager agent)

Currently a placeholder structure until real individuals and ontology rules arrive.
"""

from SensorInput import sensor_input
from model_select import model_selector
from OntologyAcess import ontology
from LLM_G import LLM_G


def run_pipeline(raw_sensor_json: dict):
    """
    Full pipeline:
    1. Parse sensor input
    2. Validate
    3. Preprocess
    4. Predict failure probability / defect category
    5. Query ontology for machine state, defect severity, employee relations
    6. Ask LLM manager to produce final assignment text
    """

    # 1. Parse
    data = sensor_input.parse(raw_sensor_json)

    # 2. Validate
    if not sensor_input.validate(data):
        return "Invalid sensor input."

    # 3. Preprocess
    data = sensor_input.preprocess(data)

    # 4. Predict using default model for now
    prediction = model_selector.predict("random_forest", data)

    # 5. Ontology lookups
    machine_id = data["machine_id"]
    machine_info = ontology.get_machine_info(machine_id)
    defect_info = ontology.get_predicted_defect_info(machine_id)
    employee_pool = ontology.get_available_employees()

    # 6. LLM manager reasoning
    manager = LLM_G()
    final_text = manager.assign_task(
        machine=machine_id,
        prediction=prediction,
        machine_info=machine_info,
        defect_info=defect_info,
        employees=employee_pool,
    )

    return final_text


if __name__ == "__main__":
    # Placeholder test
    sample = {
        "machine_id": "M3",
        "temperature": 72.4,
        "vibration": 3.1,
        "pressure": 12.0,
        "noise": 55.2
    }

    result = run_pipeline(sample)
    print(result)
