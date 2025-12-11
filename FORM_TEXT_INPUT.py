# FORM_TEXT_INPUT.py
# Módulo para entrada estruturada baseada em texto para o Projeto MORA.

import re

class FormTextInput:
    """
    Classe responsável por interpretar entradas textuais como:
    - descrição de máquinas
    - defeitos previstos
    - gravidade
    - funcionários
    - estados
    - solicitações gerais para a LLM gerente

    A saída é sempre um dicionário padronizado.
    """

    def __init__(self):
        # Palavras-chave básicas — serão expandidas com Ontology Access
        self.keywords = {
            "machine": ["m", "machine", "máquina"],
            "employee": ["func", "funcionário", "worker", "emp"],
            "defect": ["defeito", "defect", "falha", "erro"],
            "severity": ["gravidade", "severity", "nível"],
            "state": ["estado", "state", "condição"]
        }

    # -------------------------------------------------------------
    # Função principal: interpreta entrada textual
    # -------------------------------------------------------------
    def parse(self, text: str) -> dict:
        """
        Interpreta entrada textual e retorna um dicionário padronizado:
        {
            "machines": [...],
            "defects": [...],
            "severity": [...],
            "employees": [...],
            "requests": [...]
        }
        """

        text = text.lower().strip()

        result = {
            "machines": [],
            "defects": [],
            "severity": [],
            "employees": [],
            "states": [],
            "requests": [],
            "raw": text
        }

        # Expressões simples para detectar padrões
        machine_pattern = r"m[0-9]+"
        employee_pattern = r"func[a-z]*\s*[a-z]?"
        severity_pattern = r"(baixa|média|alta|critica|crítica|grave)"
        defect_pattern = r"(motor|sensor|aquecimento|vibração|vibracao|desalinhamento|falha geral)"

        # Máquinas
        machines = re.findall(machine_pattern, text)
        if machines:
            result["machines"].extend(machines)

        # Funcionários
        employees = re.findall(employee_pattern, text)
        if employees:
            result["employees"].extend(employees)

        # Gravidade
        severity = re.findall(severity_pattern, text)
        if severity:
            result["severity"].extend(severity)

        # Defeitos
        defects = re.findall(defect_pattern, text)
        if defects:
            result["defects"].extend(defects)

        # Estados podem ser detectados por palavras
        states_keywords = ["normal", "ok", "alerta", "perigo", "crítico", "quase quebrando"]
        for word in states_keywords:
            if word in text:
                result["states"].append(word)

        # Pedido geral
        if "distribuir" in text or "alocar" in text or "enviar" in text:
            result["requests"].append("allocate")

        return result

    # -------------------------------------------------------------
    # Converte estrutura para um prompt legível pela LLM
    # -------------------------------------------------------------
    def to_prompt(self, parsed: dict) -> str:
        """
        Gera um prompt textual limpo para LLM_G usar no raciocínio.
        """
        lines = ["Entrada Estruturada:"]
        
        if parsed["machines"]:
            lines.append(f"- Máquinas citadas: {', '.join(parsed['machines'])}")

        if parsed["defects"]:
            lines.append(f"- Defeitos identificados: {', '.join(parsed['defects'])}")

        if parsed["severity"]:
            lines.append(f"- Gravidade mencionada: {', '.join(parsed['severity'])}")

        if parsed["states"]:
            lines.append(f"- Estados detectados: {', '.join(parsed['states'])}")

        if parsed["employees"]:
            lines.append(f"- Funcionários referidos: {', '.join(parsed['employees'])}")

        if parsed["requests"]:
            lines.append(f"- Solicitações identificadas: {', '.join(parsed['requests'])}")

        return "\n".join(lines)


# Instância global
form_text_input = FormTextInput()
