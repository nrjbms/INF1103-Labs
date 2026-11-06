import json
from inventory import Inventory
from supplier import Supplier
from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from order import Order

FILENAME: str = "inventory.json"


def title_display():
    print("=" * 50)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50)


# ---------- File handling ----------
def find_supplier(suppliers: list[Supplier], supplier_id: str):
    for supplier in suppliers:
        if supplier.get_supplier_id().lower() == supplier_id.lower():
            return supplier
    return None


def create_product_from_dict(item: dict, suppliers: list[Supplier]):

    supplier = find_supplier(suppliers, item["supplier_id"])
    if supplier is None:
        raise ValueError(f"Unknown supplier: {item['supplier_id']}")
    if item["type"] == "physical":
        return PhysicalProduct(item["product_id"], item["name"], item["price"],
                               item["stock"], supplier, item["weight"])
    if item["type"] == "digital":
        return DigitalProduct(item["product_id"], item["name"], item["price"],
                              item["stock"], supplier, item["download_size"])
    raise ValueError(f"Unknown product type: {item['type']}")


def load_data(inventory: Inventory, suppliers: list[Supplier]):
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
            
        loaded_suppliers = [Supplier(s["supplier_id"], s["name"], s["contact_email"])
                            for s in data["suppliers"]]
        loaded_products = [create_product_from_dict(item, loaded_suppliers)
                           for item in data["products"]]
        
        suppliers.extend(loaded_suppliers)
        
        for product in loaded_products:
            inventory.add_product(product)
            
        print(f"Loaded {len(loaded_suppliers)} supplier(s) and "
              f"{len(loaded_products)} product(s) from {FILENAME}.")
        
    except FileNotFoundError:
        print("No saved data found. Starting with an empty inventory.")
        
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        print("Saved file is damaged or in an old format. Starting with an empty inventory.")


def save_data(inventory: Inventory, suppliers: list[Supplier]):
    data = {"suppliers": [supplier.supplier_dict() for supplier in suppliers],
            "products": [product.product_dict() for product in inventory.get_products()],}
    
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {FILENAME}.")


def add_supplier_menu(suppliers: list[Supplier]):
    while True:
        name = input("Supplier Name: ").strip()
        if name == "":
            print("Name cannot be empty.")
        else:
            break

    while True:
        email = input("Contact Email: ").strip()
        if "@" not in email or "." not in email:
            print("Please enter a valid email address.")
        else:
            break

    number = len(suppliers) + 1
    supplier_id = f"S{number:03d}"
    
    while find_supplier(suppliers, supplier_id):
        number += 1
        supplier_id = f"S{number:03d}"

    suppliers.append(Supplier(supplier_id, name, email))
    print(f"Supplier added with ID {supplier_id}.")


def display_suppliers_menu(suppliers: list[Supplier]):
    if len(suppliers) == 0:
        print("No suppliers yet.")
        return
    print("\n--- Suppliers ---")
    for supplier in suppliers:
        supplier.display_information()


# ---------- Product menus ----------
def add_product_menu(inventory: Inventory, suppliers: list[Supplier]):
    if len(suppliers) == 0:
        print("Add a supplier first (menu option 6).")
        return

    while True:
        print("Product type:")
        print("  1. Physical product")
        print("  2. Digital product")
        type_choice = input("Choose type (1-2): ").strip()
        if type_choice in ("1", "2"):
            break
        print("Please enter 1 or 2.")

    while True:
        name = input("Product name: ").strip()
        if name == "":
            print("Name cannot be empty.")
        else:
            break

    while True:
        try:
            price = float(input("Enter price: "))
            if price < 0:
                print("Price cannot be negative.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            stock = int(input("Stock quantity: "))
            if stock < 0:
                print("Stock cannot be negative.")
            else:
                break
        except ValueError:
            print("Please enter a whole number.")

    display_suppliers_menu(suppliers)
    while True:
        supplier = find_supplier(suppliers, input("Enter supplier ID: ").strip())
        if supplier is None:
            print("Supplier not found. Please enter an ID from the list.")
        else:
            break

    product_id = inventory.generate_id()

    if type_choice == "1":
        while True:
            try:
                weight = float(input("Enter weight (kg): "))
                if weight < 0:
                    print("Weight cannot be negative.")
                else:
                    break
            except ValueError:
                print("Please enter a valid number.")
        product: Product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        while True:
            try:
                download_size = float(input("Enter download size (MB): "))
                if download_size < 0:
                    print("Download size cannot be negative.")
                else:
                    break
            except ValueError:
                print("Please enter a valid number.")
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)

    if inventory.add_product(product):
        print(f"Product added with ID {product_id}.")


def update_stock_menu(inventory: Inventory):
    term = input("Enter product ID or name: ").strip()
    product = inventory.search_product(term)
    if product is None:
        print("Product not found.")
        return

    while True:
        try:
            quantity = int(input("Enter quantity to add (negative to remove): "))
            break
        except ValueError:
            print("Please enter a whole number.")

    if product.update_stock(quantity):
        print("Stock updated.")
        product.display_information()


def search_product_menu(inventory: Inventory):
    term = input("Enter product ID or name: ").strip()
    product = inventory.search_product(term)
    if product is None:
        print("Product not found.")
    else:
        product.display_information()
        print(f"    Fulfilment: {product.get_fulfilment_info()}")


def remove_product_menu(inventory: Inventory):
    product_id = input("Enter product ID to remove: ").strip()
    removed = inventory.remove_product(product_id)
    if removed is None:
        print("Product not found.")
    else:
        print(f"Removed {removed.get_name()} from the inventory.")


# ---------- Order menu ----------
def create_order_menu(inventory: Inventory, orders: list[Order]):
    if len(inventory.get_products()) == 0:
        print("Inventory is empty. Add products before creating an order.")
        return

    order = Order(f"O{len(orders) + 1:03d}")
    print("Add products to the order (leave blank to finish).")
    while True:
        term = input("Product ID or name: ").strip()
        if term == "":
            break
        product = inventory.search_product(term)
        if product is None:
            print("Product not found.")
            continue

        while True:
            try:
                quantity = int(input(f"Quantity of {product.get_name()}: "))
                if quantity <= 0:
                    print("Quantity must be at least 1.")
                elif quantity > product.get_stock():
                    print(f"Only {product.get_stock()} in stock.")
                else:
                    break
            except ValueError:
                print("Please enter a whole number.")
        order.add_order_line(product, quantity)
        print("Line added.")

    if len(order.get_order_lines()) == 0:
        print("Order cancelled (no lines).")
        return
    orders.append(order)
    order.display_information()



def main():
    title_display()
    inventory = Inventory()
    suppliers: list[Supplier] = []
    orders: list[Order] = []
    load_data(inventory, suppliers)

    while True:
        print("\n----------- MENU -----------")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Remove a product")
        print("6. Add a supplier")
        print("7. Display suppliers")
        print("8. Create an order")
        print("9. Save data")
        print("10. Exit")
        print("----------------------------")
        choice = input("\nEnter Option (1-10): ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_menu(inventory, suppliers)
        elif choice == "3":
            update_stock_menu(inventory)
        elif choice == "4":
            search_product_menu(inventory)
        elif choice == "5":
            remove_product_menu(inventory)
        elif choice == "6":
            add_supplier_menu(suppliers)
        elif choice == "7":
            display_suppliers_menu(suppliers)
        elif choice == "8":
            create_order_menu(inventory, orders)
        elif choice == "9":
            save_data(inventory, suppliers)
        elif choice == "10":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-10.")


main()