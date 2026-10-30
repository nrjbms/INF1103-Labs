from product import Product


class DigitalProduct(Product):
    
    def __init__(self, product_id, name, price, stock, download_size):
            super().__init__(product_id, name, price, stock)
            self.__download_size = download_size
            
    def get_download_size(self):
        return self.__download_size
            
    def display_information(self):
            super().display_information()
            print(f"Type: Digital | Download Size: {self.__download_size} MB")
            
    def get_fulfilment_info(self):
            return "Delivered digitally."
            
    def product_dict(self):
        data = super().product_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data