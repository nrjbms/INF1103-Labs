from product import Product

class OrderLine:
    
    def __init__(self, product: Product, quantity):
        self.__product = product
        self.__quantity = quantity

    def get_product(self):
        return self.__product

    def get_quantity(self):
        return self.__quantity

    def calculate_line_total(self):
        return self.__product.get_price() * self.__quantity
    
    def display_information(self):
        self.__product.display_information()
        print(f" Quantity: {self.__quantity} | Line Total: ${self.calculate_line_total():.2f}")