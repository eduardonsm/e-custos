class Product:
    def __init__(self, name, dateProject, dateStart, isActive, endTime, price, productTree, id=None):
        
        self.name = name
        self.dateProject = dateProject
        self.dateStart = dateStart
        self.isActive = isActive
        self.endTime = endTime
        self.price = price
        self.productTree = productTree
        self.id = id
