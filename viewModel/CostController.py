from model.CostRepository import CostRepository
from model.Cost import Cost

class CostController:
    def __init__(self, repo=None):
        self.repo = repo or CostRepository()

    def create_cost(self, code, product, description, quantity, unitPrice, is_fixo, is_direto, is_relevante, is_eliminavel, is_oculto):
        cost = Cost(code, product, description, quantity, unitPrice, is_fixo, is_direto, is_relevante, is_eliminavel, is_oculto)
        return cost

    def add_cost(self, code, product, description, quantity, unitPrice, is_fixo, is_direto, is_relevante, is_eliminavel, is_oculto, user_id):
        cost = self.create_cost(code, product, description, quantity, unitPrice, is_fixo, is_direto, is_relevante, is_eliminavel, is_oculto)
        return CostRepository.add_cost(self.repo, cost, user_id)
    def get_costs_by_user(self, user_id):
        return CostRepository.get_costs_by_user(self.repo, user_id)
    def get_cost_by_code(self, code, user_id):
        return CostRepository.get_cost_by_code(self.repo, code, user_id)
    def update_cost(self,code, productId, description, quantity, unitPrice, is_fixo, is_direto, is_relevante, is_eliminavel, is_oculto, user_id):
        return CostRepository.update_cost(self.repo, code, productId, description, quantity, unitPrice, is_fixo, is_direto, is_relevante, is_eliminavel, is_oculto, user_id)
    def delete_cost(self,code,user_id):
        return CostRepository.delete_cost(self.repo, code, user_id)
