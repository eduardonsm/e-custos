import sys
import os
import pytest
import json
import sqlite3

# Garante que o caminho está correto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.ProductRepository import ProductRepository
from model.Product import Product

@pytest.fixture
def repo():
    conn = sqlite3.connect(":memory:")
    repo = ProductRepository(conn=conn)
    repo.create_dbProducts()
    return repo

@pytest.fixture
def sample_product():
    return Product(
        name="Produto Teste",
        dateProject="2023-10-01",
        dateStart="2023-10-02",
        isActive=True,
        endTime="2023-12-31",
        price=99.99,
        productTree=json.dumps({"tree": "data"})
    )

def test_add_product(repo, sample_product):
    assert repo.add_product(sample_product, user_id=1)

def test_get_products_by_user(repo, sample_product):
    repo.add_product(sample_product, 1)
    products = repo.get_products_by_user(1)
    assert len(products) == 1
    assert products[0].name == "Produto Teste"

def test_get_product_by_id(repo, sample_product):
    repo.add_product(sample_product, 1)
    product = repo.get_product_by_id(1, 1)
    assert product is not None
    assert product.name == "Produto Teste"

def test_update_product(repo, sample_product):
    repo.add_product(sample_product, 1)
    updated = repo.update_product(
        1, 1, "Produto Editado", "2023-11-01", "2023-11-02", True,
        "2024-01-01", 150.0, json.dumps({"tree": "nova"})
    )
    assert updated
    product = repo.get_product_by_id(1, 1)
    assert product.name == "Produto Editado"

def test_delete_product(repo, sample_product):
    repo.add_product(sample_product, 1)
    deleted = repo.delete_product(1, 1)
    assert deleted
    assert repo.get_product_by_id(1, 1) is None
