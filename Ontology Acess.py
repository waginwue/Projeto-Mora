# OntologyAcess.py
# Template de acesso à ontologia para o Projeto-Mora

from owlready2 import get_ontology, default_world

class OntologyAccess:
    def __init__(self, path: str):
        self.path = path
        self.onto = None

    def load(self):
        """Carrega a ontologia OWL"""
        try:
            self.onto = get_ontology(self.path).load()
            return True
        except Exception as e:
            print(f"Erro ao carregar ontologia: {e}")
            return False

    def get_machines(self):
        """Retorna indivíduos do tipo Máquina"""
        if not self.onto:
            return []
        return list(self.onto.Machine.instances()) if hasattr(self.onto, "Machine") else []

    def get_employees(self):
        """Retorna indivíduos do tipo Funcionário"""
        if not self.onto:
            return []
        return list(self.onto.Employee.instances()) if hasattr(self.onto, "Employee") else []

    def get_break_risk(self, machine):
        """Obtém risco de quebra anotado na ontologia (datatype property)."""
        try:
            return machine.breakRisk[0] if hasattr(machine, "breakRisk") else None
        except:
            return None

    def get_defect_severity(self, machine):
        """Obtém severidade do defeito previsto (datatype property)."""
        try:
            return machine.defectSeverity[0] if hasattr(machine, "defectSeverity") else None
        except:
            return None

    def classify_machine_status(self, machine):
        """
        Classifica a máquina com base no risco de quebra e severidade.
        - risco < 0.3 → normal
        - 0.3 ≤ risco < 0.7 → aproximando de quebrar
        - risco ≥ 0.7 → crítico
        """
        risk = self.get_break_risk(machine)
        severity = self.get_defect_severity(machine)

        if risk is None:
            return "desconhecido"

        if risk < 0.3:
            return "normal"
        elif risk < 0.7:
            return "aproximando de quebrar"
        return "critico"

    def select_employees_for_machine(self, machine, employees):
        """
        Seleciona funcionários baseado na gravidade.
        Regras:
        - status normal → nenhum funcionário
        - aproximando → funcionário júnior sozinho
        - crítico → 1 sênior + 1 treinando
        """
        status = self.classify_machine_status(machine)

        juniors = [e for e in employees if "Junior" in e.is_a[0].name]
        seniors = [e for e in employees if "Senior" in e.is_a[0].name]
        trainees = [e for e in employees if "Trainee" in e.is_a[0].name]

        if status == "normal":
            return []
        elif status == "aproximando de quebrar":
            return juniors[:1] if juniors else []
        elif status == "critico":
            team = []
            if seniors:
                team.append(seniors[0])
            if trainees:
                team.append(trainees[0])
            return team
        return []
