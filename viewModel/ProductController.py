from model.ProductRepository import ProductRepository
from model.Product import Product

class ProductController:
    def __init__(self, repo=None):
        self.repo = repo or ProductRepository()
    
    def add_product(self, name, dateProject, dateStart, isActive, endTime, price, productTree, user_id):
        product = Product(name, dateProject, dateStart, isActive, endTime, price, productTree)
        return ProductRepository.add_product(product, user_id)

    def get_products_by_user(self, user_id):
        return ProductRepository.get_products_by_user(user_id)

    def get_product_by_id(self, product_id, user_id):
        return ProductRepository.get_product_by_id(product_id, user_id)

    def update_product(self, product_id, user_id, name, dateProject, dateStart, isActive, endTime, price, productTree):
        return ProductRepository.update_product(product_id, user_id, name, dateProject, dateStart, isActive, endTime, price, productTree)

    def delete_product(self, product_id, user_id):
        return ProductRepository.delete_product(product_id, user_id)
