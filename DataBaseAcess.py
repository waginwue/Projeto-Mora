# DataBaseAcess.py
"""
Database access layer for Projeto-Mora.
This is a placeholder version that simulates database operations until
real DB schema and connection details are provided.

It supports:
- fetching machine records
- storing predictions
- retrieving employees
- updating machine state

Later this can be replaced by PostgreSQL, MySQL, SQLite, or ORM (SQLAlchemy).
"""

from typing import Dict, Any, List

class DataBaseAccess:
    def __init__(self):
        # Placeholder in-memory simulated database
        self.machines = {
            "M1": {"state": "normal", "last_prediction": None},
            "M2": {"state": "stable", "last_prediction": None},
            "M3": {"state": "warning", "last_prediction": None},
        }

        self.employees = [
            {"name": "A", "role": "senior"},
            {"name": "B", "role": "trainee"},
            {"name": "C", "role": "junior"},
        ]

    # ----------------------------------------------------------------------
    # Machine operations
    # ----------------------------------------------------------------------
    def get_machine(self, machine_id: str) -> Dict[str, Any]:
        return self.machines.get(machine_id, None)

    def update_machine_state(self, machine_id: str, new_state: str):
        if machine_id in self.machines:
            self.machines[machine_id]["state"] = new_state

    def save_prediction(self, machine_id: str, prediction: Dict[str, Any]):
        if machine_id in self.machines:
            self.machines[machine_id]["last_prediction"] = prediction

    # ----------------------------------------------------------------------
    # Employee operations
    # ----------------------------------------------------------------------
    def get_employees(self) -> List[Dict[str, str]]:
        return self.employees

    def get_employees_by_role(self, role: str) -> List[Dict[str, str]]:
        return [e for e in self.employees if e["role"] == role]


# Global instance
DB = DataBaseAccess()
