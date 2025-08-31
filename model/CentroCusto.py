class CentroCusto:
    TIPOS = ['Produtivo', 'Auxiliar', 'Administrativo']
    
    def __init__(self, descricao: str, tipo: str, quantidade_postos: int, 
                 capacidade_horas: float, capacidade_itens: int, user_id: int, 
                 centro_id: int = None):
        """
        Construtor da classe CentroCusto
        
        Args:
            descricao: Descrição do centro de custo
            tipo: 'Produtivo', 'Auxiliar' ou 'Administrativo'
            quantidade_postos: Número de postos de trabalho
            capacidade_horas: Capacidade diária em horas
            capacidade_itens: Capacidade diária em itens
            user_id: ID do usuário responsável
            centro_id: ID único (opcional para novos centros)
        """
        self.id = centro_id
        self.descricao = descricao
        self.tipo = tipo
        self.quantidade_postos = quantidade_postos
        self.capacidade_horas = capacidade_horas
        self.capacidade_itens = capacidade_itens
        self.user_id = user_id