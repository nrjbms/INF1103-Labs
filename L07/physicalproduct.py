from product import Product

class PhysicalProduct(Product):
    
    SHIPPING = 5.00
    COST_PER_KG = 2.00
    
    def __init__(self, product_id, name, price, stock,weight):
        super().__init__(self, product_id, name, price, stock)
        self.__weight = weight
 
    def get_weight(self):
        return self.__weight
 
    def display_information(self):
        super().display_information()
        print(f"Type: Physical | Weight: {self.__weight} kg")
 
    def get_fulfilment_info(self):
        return "Requires physical shipping."
 
    def calculate_shipping_cost(self):
        return self.SHIPPING + self.COST_PER_KG * self.__weight
 
    def product_dict(self):
        data = super().product_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data