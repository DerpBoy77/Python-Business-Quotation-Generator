class Product:
    def __init__(self, data):
        self.sku = data[0]
        self.productName = data[1]
        self.defaultPrice = data[2]
