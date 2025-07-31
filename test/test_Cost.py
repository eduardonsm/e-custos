import sys
import os
import pytest
import json
import sqlite3

# Garante que o caminho está correto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.CostRepository import CostRepository
from model.Cost import Cost

@pytest.fixture
def repo():
    conn = sqlite3.connect(":memory:")
    repo = CostRepository(conn=conn)
    repo.create_dbCosts()
    return repo

@pytest.fixture
def sample_cost():
    return Cost(
        code=1,
        product=1,
        description="Custo Teste",
        quantity=10,
        unitPrice=5.0,
        is_fixo=True,
        is_direto=False,
        is_relevante=True,
        is_eliminavel=False,
        is_oculto=False
    )

def test_add_cost(repo, sample_cost):
    assert repo.add_cost(sample_cost, user_id=1)

# def test_get_costs_by_user(repo, sample_cost):
#     repo.add_cost(sample_cost, user_id=1)
#     costs = repo.get_costs_by_user(1)
#     assert len(costs) == 1
#     assert costs[0].description == "Custo Teste"

# def test_get_cost_by_id(repo, sample_cost):
#     repo.add_cost(sample_cost, user_id=1)
#     cost = repo.get_cost_by_id(1, 1)
#     assert cost is not None
#     assert cost.description == "Custo Teste"

# def test_update_cost(repo, sample_cost):
    

# def test_delete_cost(repo, sample_cost):
    