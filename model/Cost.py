class Cost:
    def __init__(self, code, product, description, quantity, unitPrice, is_fixo, is_direto, is_relevante, is_eliminavel, is_oculto):
        self.code = code
        self.product = product
        self.description = description
        self.quantity = quantity
        self.unitPrice = unitPrice
        self.totalPrice = unitPrice * quantity
        self.is_fixo = is_fixo
        self.is_direto = is_direto
        self.is_relevante = is_relevante
        self.is_eliminavel = is_eliminavel
        self.is_oculto = is_oculto
    