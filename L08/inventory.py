class Inventory:

    def __init__(self):
        self.__products = []

    def generate_id(self):
        highest = 0
        for product in self.__products:
            number = product.get_product_id()[1:]
            if number.isdigit() and int(number) > highest:
                highest = int(number)
        return f"P{highest + 1:03d}"

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            print("Error: a product with that ID already exists.")
            return False
        self.__products.append(product)
        return True

    def search_product(self, search_term):
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
        print("\n--- Inventory ---")
        for product in self.__products:
            product.display_information()

    def get_products(self):
        return list(self.__products)