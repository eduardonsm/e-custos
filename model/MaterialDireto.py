class MaterialDireto:
    FONTES = ['Fornecido', 'Produzido']
    UNIDADES_TEMPO = ['Horas', 'Dias', 'Semanas', 'Meses']
    
    def __init__(self, descricao: str, fonte: str, lead_time_producao: str, 
                 lead_time_fornecimento: str, fornecedor: str, valor_unitario: float,
                 estoque_atual: int, estoque_minimo: int, estoque_maximo: int,
                 user_id: int, material_id: int = None):
        """
        Construtor da classe MaterialDireto
        
        Args:
            descricao: Descrição do material
            fonte: 'Fornecido' ou 'Produzido'
            lead_time_producao: Tempo de produção (com unidade)
            lead_time_fornecimento: Tempo de fornecimento (com unidade)
            fornecedor: Nome do fornecedor
            valor_unitario: Valor por unidade
            estoque_atual: Quantidade atual em estoque
            estoque_minimo: Ponto de reposição
            estoque_maximo: Capacidade máxima
            user_id: ID do usuário responsável
            material_id: ID único (opcional para novos materiais)
        """
        self.id = material_id
        self.descricao = descricao
        self.fonte = fonte
        self.lead_time_producao = lead_time_producao
        self.lead_time_fornecimento = lead_time_fornecimento
        self.fornecedor = fornecedor
        self.valor_unitario = valor_unitario
        self.estoque_atual = estoque_atual
        self.estoque_minimo = estoque_minimo
        self.estoque_maximo = estoque_maximo
        self.user_id = user_id
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id': self.id,
            'descricao': self.descricao,
            'fonte': self.fonte,
            'lead_time_producao': self.lead_time_producao,
            'lead_time_fornecimento': self.lead_time_fornecimento,
            'fornecedor': self.fornecedor,
            'valor_unitario': self.valor_unitario,
            'estoque_atual': self.estoque_atual,
            'estoque_minimo': self.estoque_minimo,
            'estoque_maximo': self.estoque_maximo,
            'user_id': self.user_id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Cria a partir de um dicionário"""
        return cls(
            material_id=data.get('id'),
            descricao=data['descricao'],
            fonte=data['fonte'],
            lead_time_producao=data['lead_time_producao'],
            lead_time_fornecimento=data['lead_time_fornecimento'],
            fornecedor=data['fornecedor'],
            valor_unitario=data['valor_unitario'],
            estoque_atual=data['estoque_atual'],
            estoque_minimo=data['estoque_minimo'],
            estoque_maximo=data['estoque_maximo'],
            user_id=data['user_id']
        )