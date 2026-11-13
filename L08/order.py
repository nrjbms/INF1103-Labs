from orderline import OrderLine
from product import Product

class Order:
    
    def __init__(self, order_id: str):   
        self.__order_id = order_id
        self.__order_lines: list[OrderLine] = []
        
    def get_order_id(self):
        return self.__order_id
    
    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)
    
    def remove_order_line(self, order_line):
        if order_line in self.__order_lines:
            self.__order_lines.remove(order_line)
            return True
        return False
    
    def calculate_order_total(self) -> float:
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_line_total()
        return total   
    
    def display_information(self):
        print(f"Order ID: {self.__order_id}")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"Order Total: ${self.calculate_order_total():.2f}")
