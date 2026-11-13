from product import Product


class Inventory:

    def __init__(self):
        self.__products: list[Product] = []

    def generate_id(self):
        highest = 0
        for product in self.__products:
            number = product.get_product_id()[1:]
            if number.isdigit() and int(number) > highest:
                highest = int(number)
        return f"P{highest + 1:03d}"

    def add_product(self, product: Product) -> bool:
        if self.search_product(product.get_product_id()) is not None:
            print("Error: a product with that ID already exists.")
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                self.__products.remove(product)
                return product
        return None

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def search_product(self, search_term: str) -> Product | None:
        search_term = search_term.lower()
        for product in self.__products:
            if (product.get_product_id().lower() == search_term
                    or product.get_name().lower() == search_term):
                return product
        return None

    def display_all(self):
        if len(self.__products) == 0:
            print("Inventory is empty.")
            return
        print("\nInventory")
        print("-" * 30)
        for product in self.__products:
            product.display_information()

    def get_products(self) -> list[Product]:
        return list(self.__products)