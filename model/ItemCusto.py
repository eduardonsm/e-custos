class ItemCusto:
    CATEGORIAS = ['MD', 'MOD', 'CIF', 'CO']
    CLASSIFICACOES = ['Variável', 'Fixo']
    UNIDADES_MEDIDA = ['Unid', 'ml', 'litros', 'kg', 'kW/h', 'h']
    
    def __init__(self, produto_id: str, quantidade: float, medida: str, 
                 descricao: str, valor_unitario: float, valor_total: float,
                 categoria: str, classificacao: str, user_id: int, item_id: int = None):
        """
        Construtor da classe ItemCusto
        
        Args:
            produto_id: ID do produto relacionado ('CV-001', 'CA-002', 'Nenhum', etc.)
            quantidade: Quantidade utilizada
            medida: Unidade de medida (Unid, ml, litros, kg, kW/h, h)
            descricao: Descrição do item de custo
            valor_unitario: Valor por unidade
            valor_total: Valor total (quantidade × valor_unitario)
            categoria: 'MD', 'MOD', 'CIF' ou 'CO'
            classificacao: 'Variável' ou 'Fixo'
            user_id: ID do usuário responsável
            item_id: ID único (opcional para novos itens)
        """
        self.id = item_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.medida = medida
        self.descricao = descricao
        self.valor_unitario = valor_unitario
        self.valor_total = valor_total
        self.categoria = categoria
        self.classificacao = classificacao
        self.user_id = user_id
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'quantidade': self.quantidade,
            'medida': self.medida,
            'descricao': self.descricao,
            'valor_unitario': self.valor_unitario,
            'valor_total': self.valor_total,
            'categoria': self.categoria,
            'classificacao': self.classificacao,
            'user_id': self.user_id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Cria a partir de um dicionário"""
        return cls(
            item_id=data.get('id'),
            produto_id=data['produto_id'],
            quantidade=data['quantidade'],
            medida=data['medida'],
            descricao=data['descricao'],
            valor_unitario=data['valor_unitario'],
            valor_total=data['valor_total'],
            categoria=data['categoria'],
            classificacao=data['classificacao'],
            user_id=data['user_id']
        )
    
    def calcular_valor_total(self):
        """Calcula o valor total baseado na quantidade e valor unitário"""
        self.valor_total = self.quantidade * self.valor_unitario
        return self.valor_total