# LLM_G.py

class LLMGerente:
    """
    Primeira versão do gerente LLM lógico baseado em regras.
    Quando chegarem os dados reais, substituímos a lógica interna.
    """

    def __init__(self, rf_engine=None, lstm_engine=None):
        self.rf = rf_engine
        self.lstm = lstm_engine

    # -----------------------------------------------------------
    # Função principal acionada pelo FastAPI
    # -----------------------------------------------------------
    def processar(self, mensagem: str, contexto_extra=None):
        """
        Recebe um pedido do usuário e gera um relatório no estilo especificado.
        """

        # Por enquanto apenas simulação usando regras
        maquinas = self._simular_estado_maquinas()
        funcionarios = self._simular_funcionarios()

        relatorio = self._gerar_relatorio(maquinas, funcionarios)
        return relatorio

    # -----------------------------------------------------------
    # Simulações temporárias (até você enviar os dados reais)
    # -----------------------------------------------------------
    def _simular_estado_maquinas(self):
        """
        Simulação de máquinas com 'risco de quebrar' e 'gravidade prevista'.
        """

        # risco: 0 = normal, 1 = leve, 2 = moderado, 3 = alto
        # gravidade do defeito: 0 = simples, 1 = médio, 2 = crítico
        return {
            "M1": {"risco": 0, "gravidade": 0},
            "M2": {"risco": 1, "gravidade": 0},
            "M3": {"risco": 2, "gravidade": 1},
        }

    def _simular_funcionarios(self):
        return {
            "A": {"tipo": "sênior"},
            "B": {"tipo": "treinando"},
            "C": {"tipo": "júnior"}
        }

    # -----------------------------------------------------------
    # Regras para decidir equipe de manutenção
    # -----------------------------------------------------------
    def _definir_equipe(self, risco, gravidade, funcionarios):
        """
        Retorna uma equipe baseada nas regras:
        - júnior vai sozinho em casos simples
        - treinando acompanha sênior em casos não urgentes
        - sênior sempre atua em casos de risco moderado ou maior
        """

        if risco == 0 and gravidade == 0:
            return None  # sem necessidade

        if risco == 1 and gravidade == 0:
            # caso leve
            junior = self._buscar_tipo(funcionarios, "júnior")
            return [junior]

        if risco == 2 or (risco == 1 and gravidade == 1):
            # caso moderado
            senior = self._buscar_tipo(funcionarios, "sênior")
            treinando = self._buscar_tipo(funcionarios, "treinando")
            return [senior, treinando]

        if risco >= 3 or gravidade >= 2:
            # crítico
            senior = self._buscar_tipo(funcionarios, "sênior")
            return [senior]

    def _buscar_tipo(self, funcionarios, tipo):
        for nome, info in funcionarios.items():
            if info["tipo"] == tipo:
                return nome
        return None

    # -----------------------------------------------------------
    # Gera o relatório no estilo solicitado
    # -----------------------------------------------------------
    def _gerar_relatorio(self, maquinas, funcionarios):
        relatorio = []

        for maquina, dados in maquinas.items():
            risco = dados["risco"]
            gravidade = dados["gravidade"]

            # Define status textual
            if risco == 0:
                status = "está normal"
            elif risco == 1:
                status = "ainda está longe de quebrar"
            elif risco == 2:
                status = "está se aproximando de quebrar"
            else:
                status = "está prestes a quebrar"

            equipe = self._definir_equipe(risco, gravidade, funcionarios)

            # Monta frase final
            if equipe is None:
                relatorio.append(f"Máquina {maquina} {status}.")
            else:
                if len(equipe) == 1:
                    relatorio.append(
                        f"Máquina {maquina} {status}, funcionário {equipe[0]} será enviado sozinho."
                    )
                else:
                    equipe_str = " e ".join(equipe)
                    relatorio.append(
                        f"Máquina {maquina} {status}, {equipe_str} serão enviados juntos."
                    )

        return "\n".join(relatorio)
