class MaoDeObraDireta:
    def __init__(self, cargo: str, centro_custo: str, operacao: str, 
                 tempo_padrao: float, capacidade_horas: float, capacidade_itens: int,
                 custo_hora: float, user_id: int, mod_id: int = None):
        """
        Construtor da classe MaoDeObraDireta
        
        Args:
            cargo: Cargo/função do colaborador
            centro_custo: Centro de custo/departamento
            operacao: Operação realizada
            tempo_padrao: Tempo padrão por operação (horas)
            capacidade_horas: Capacidade diária em horas
            capacidade_itens: Capacidade diária em itens
            custo_hora: Custo hora-homem (salário + encargos + benefícios)
            user_id: ID do usuário responsável
            mod_id: ID único (opcional para novos registros)
        """
        self.id = mod_id
        self.cargo = cargo
        self.centro_custo = centro_custo
        self.operacao = operacao
        self.tempo_padrao = tempo_padrao
        self.capacidade_horas = capacidade_horas
        self.capacidade_itens = capacidade_itens
        self.custo_hora = custo_hora
        self.user_id = user_id
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id': self.id,
            'cargo': self.cargo,
            'centro_custo': self.centro_custo,
            'operacao': self.operacao,
            'tempo_padrao': self.tempo_padrao,
            'capacidade_horas': self.capacidade_horas,
            'capacidade_itens': self.capacidade_itens,
            'custo_hora': self.custo_hora,
            'user_id': self.user_id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Cria a partir de um dicionário"""
        return cls(
            mod_id=data.get('id'),
            cargo=data['cargo'],
            centro_custo=data['centro_custo'],
            operacao=data['operacao'],
            tempo_padrao=data['tempo_padrao'],
            capacidade_horas=data['capacidade_horas'],
            capacidade_itens=data['capacidade_itens'],
            custo_hora=data['custo_hora'],
            user_id=data['user_id']
        )