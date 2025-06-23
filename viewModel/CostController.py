from model.Cost import Cost
from model.UserRepository import UserRepository

class CostController:
    
    def create_cost(self, nome, valor, categoria, is_direto, is_fixo, is_relevante, is_eliminavel, is_oculto):
        cost = Cost(nome, valor, categoria, is_direto, is_fixo, is_relevante, is_eliminavel, is_oculto)
        return cost
    def add_cost_to_db(self, nome, valor,categoria, is_direto, is_fixo, is_relevante, is_eliminavel, is_oculto, user_id):
        cost = self.create_cost(nome, valor, categoria, is_direto, is_fixo, is_relevante, is_eliminavel, is_oculto)
        return UserRepository.add_cost(cost, user_id)
        