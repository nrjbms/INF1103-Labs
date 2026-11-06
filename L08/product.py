from abc import ABC, abstractmethod
from supplier import Supplier

class Product(ABC):

    def __init__(self, product_id, name, price, stock, supplier: Supplier):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__supplier: Supplier = supplier

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock
    
    def get_supplier(self):
        return self.__supplier

    def update_stock(self, quantity):
        if self.__stock + quantity < 0:
            print("Error: not enough stock. Stock cannot go below 0.")
            return False
        self.__stock += quantity
        return True

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock} | Supplier: {self.__supplier.get_name()}")

    def product_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.get_supplier_id()
        }
        
@abstractmethod
def get_fulfilment_info(self):
    pass