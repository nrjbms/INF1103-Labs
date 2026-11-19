from orderline import OrderLine
from product import Product
from discountstrategy import DiscountStrategy, NoDiscount

class Order:
    
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):   
        self.__order_id = order_id
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()
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
    
    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def calculate_total(self) -> float:
        total = sum(line.calculate_line_total() for line in self.__order_lines)
        return self.__discount.apply(total)

    def calculate_order_total(self) -> float:
        return self.calculate_total()   
    
    def display_information(self):
        print(f"Order ID: {self.__order_id}")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"Order Total: ${self.calculate_order_total():.2f}")
