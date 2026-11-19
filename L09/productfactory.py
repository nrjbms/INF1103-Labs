from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               weight: float = 0.0, download_size: float = 0.0) -> Product:
        product_type = product_type.strip().lower()
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, weight)
        if product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, download_size)
        raise ValueError(f"Unknown product type: {product_type}")
