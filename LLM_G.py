#LLM usada como gerente no programa
# app/agents/LLM_G.py

from openai import OpenAI
from app.ontology.ontology_loader import OntologyManager


class LLMGerente:
    """
    Agente Gerente (G)

    Responsabilidades:
    - Interpretar entradas do sistema
    - Validar defeitos, modelos, estados e gravidades com base na ontologia
    - Criar diagnósticos iniciais
    - Gerar plano de manutenção estruturado
    - Coordenar delegação para outros agentes
    """

    def __init__(self, model="gpt-4.1", ontology_path="app/ontology/ontology.owl"):
        self.client = OpenAI()
        self.model = model
        self.ontology = OntologyManager(path=ontology_path)

        print("[LLM_G] Agente Gerente inicializado.")

    # =====================================================================
    # SISTEMA
    # =====================================================================
    def build_system_prompt(self):
        o = self.ontology.get_all()

        return f"""
Você é o AGENTE GERENTE do Sistema Mora.

Base de Conhecimento (via Ontologia):
- Defeitos: {o["Defeitos"]}
- Estados: {o["Estados"]}
- Gravidades: {o["Gravidades"]}
- Modelos: {o["Modelos"]}
- Locais: {o["Locais"]}
- Durabilidades: {o["Durabilidades"]}
- Níveis Alarmantes: {o["NiveisAlarmantes"]}

Regras obrigatórias:
1. NÃO invente defeitos, estados ou gravidades fora da ontologia.
2. Sempre valide a entrada antes de gerar qualquer plano.
3. Caso haja algo inválido, explique exatamente o que e solicite correção.
4. Priorize defeitos com gravidades mais altas e estados críticos.
5. Sempre gere respostas organizadas, claras e justificadas.

Seu papel:
- Ser o gerente geral.
- Decidir prioridades.
- Criar planos de manutenção.
- Interpretar a situação operacional.
"""

    # =====================================================================
    # CONSULTA SOBRE CONHECIMENTO (Defeitos, Estados, etc)
    # =====================================================================
    def consultar(self, pergunta: str):
        """
        Perguntas gerais feitas ao Agente Gerente sobre:
        - Defeitos
        - Estados
        - Gravidades
        - Modelos
        - Regras
        - Comportamento esperado
        """

        messages = [
            {"role": "system", "content": self.build_system_prompt()},
            {"role": "user", "content": pergunta}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return response.choices[0].message["content"]

    # =====================================================================
    # PLANEJAMENTO DE MANUTENÇÃO
    # =====================================================================
    def planejar_distribuicao(self, dados: dict):
        """
        Entrada esperada:
        {
            "maquinas": [
                {
                    "id": "M01",
                    "modelo": "Maquina1",
                    "estado": "Operacional ou Quebrado",
                    "defeito": "Feixe / Laser / Etc",
                    "gravidade": "Alta / Média / Baixa",
                    "local": "Fabrica1"
                },
                ...
            ],
            "funcionarios": [...]
        }

        Saída:
        - Validação
        - Correções sugeridas
        - Plano estruturado de manutenção
        """

        user_prompt = f"""
Gere o melhor PLANO DE MANUTENÇÃO possível com base na ontologia.

Entrada:
{dados}

Tarefas:
1. Verifique se cada defeito, estado, modelo e gravidade são válidos.
2. Explique problemas encontrados.
3. Caso tudo esteja válido, gere:
   - Prioridades
   - Ordem de atendimento
   - Atribuição inicial para equipes (se possível)
   - Justificativas
"""

        messages = [
            {"role": "system", "content": self.build_system_prompt()},
            {"role": "user", "content": user_prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return response.choices[0].message["content"]

