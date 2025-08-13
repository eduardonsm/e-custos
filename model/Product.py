class Product:
    CATEGORIES = ['Acabado', 'Semiacabado', 'Componente', 'Matéria-prima']
    STATUSES = ['Ativo', 'Inativo', 'Em desenvolvimento']
    def __init__(self, description, unit, category, status, production_centers, production_flow, user_id, product_id=None):
        self.id = product_id
        self.description = description
        self.unit = unit
        self.category = category
        self.status = status
        self.production_centers = production_centers
        self.production_flow = production_flow
        self.user_id = user_id