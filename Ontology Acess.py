from owlready2 import *

class OntologyAccess:
    def __init__(self, ontology_path):
        self.onto = get_ontology(ontology_path).load()
        self._bind_classes()
        self._bind_properties()

    # ----------------------------------------------------------
    # Bind OWL Classes to Python attributes
    # ----------------------------------------------------------
    def _bind_classes(self):
        self.Maquina = self.onto.Maquina
        self.Modelo = self.onto.Modelo
        self.Estado = self.onto.Estado
        self.Gravidade = self.onto.Gravidade
        self.Defeito = self.onto.Defeito
        self.Funcionario = self.onto.Funcionario
        self.Senior = self.onto.Senior
        self.Junior = self.onto.Junior
        self.Treinando = self.onto.Treinando

    # ----------------------------------------------------------
    # Bind OWL Object Properties
    # ----------------------------------------------------------
    def _bind_properties(self):
        self.Maquina_No_Estado = self.onto.Maquina_No_Estado
        self.Maquina_Do_Modelo = self.onto.Maquina_Do_Modelo
        self.Modelo_Da_Maquina = self.onto.Modelo_Da_Maquina
        self.Defeito_De_Gravidade = self.onto.Defeito_De_Gravidade
        self.Treinado_por = self.onto.Treinado_por
        self.Treinando_prop = self.onto.Treinando

    # ----------------------------------------------------------
    # HIGH-LEVEL QUERY FUNCTIONS FOR THE LLM
    # ----------------------------------------------------------

    # --- MACHINE QUERIES -------------------------------------------------

    def get_all_machines(self):
        return list(self.Maquina.instances())

    def get_machine_state(self, machine):
        if machine.Maquina_No_Estado:
            return machine.Maquina_No_Estado[0]
        return None

    def get_machine_model(self, machine):
        if machine.Maquina_Do_Modelo:
            return machine.Maquina_Do_Modelo[0]
        return None

    # --- DEFECT + GRAVITY ------------------------------------------------

    def get_defect_gravity(self, defect):
        if defect.Defeito_De_Gravidade:
            return defect.Defeito_De_Gravidade[0]
        return None

    # --- EMPLOYEE QUERIES ------------------------------------------------

    def get_all_employees(self):
        return list(self.Funcionario.instances())

    def get_seniors(self):
        return list(self.Senior.instances())

    def get_juniors(self):
        return list(self.Junior.instances())

    def get_trainees(self):
        return list(self.Treinando.instances())

    def get_trainee_trainer(self, trainee):
        if trainee.Treinado_por:
            return trainee.Treinado_por[0]
        return None

    # --- GENERIC UTILITY -------------------------------------------------

    def describe_individual(self, ind):
        """Return class name and relationships (debug for LLM)."""
        desc = {
            "name": ind.name,
            "classes": [c.name for c in ind.is_a],
            "relations": {}
        }
        for prop in self.onto.object_properties():
            values = prop[ind]
            if values:
                desc["relations"][prop.name] = [v.name for v in values]
        return desc

    def debug_print(self):
        """Prints all machines and employees for debugging."""
        print("=== Machines ===")
        for m in self.get_all_machines():
            print(m.name, "| State:", self.get_machine_state(m), "| Model:", self.get_machine_model(m))

        print("\n=== Employees ===")
        for e in self.get_all_employees():
            print(self.describe_individual(e))
