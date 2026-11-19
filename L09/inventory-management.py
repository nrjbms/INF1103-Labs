import json
import csv
from inventory import Inventory
from supplier import Supplier
from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from order import Order
from productfactory import ProductFactory
from discountstrategy import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount

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
    return ProductFactory.create(item["type"], item["product_id"], item["name"],
                                 float(item["price"]), int(item["stock"]), supplier,
                                 weight=float(item.get("weight", 0)),
                                 download_size=float(item.get("download_size", 0)))


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


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="", encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.DictReader(file)
            for row_number, row in enumerate(reader, start=2):
                try:
                    product = ProductFactory.create(
                        row["product_type"], row["product_id"], row["name"],
                        float(row["price"]), int(row["stock_quantity"]), supplier,
                        weight=float(row.get("weight") or 0),
                        download_size=float(row.get("download_size") or 0))
                    if not inventory.add_product(product):
                        print(f"Skipping row {row_number}: duplicate product ID")
                        continue
                    loaded += 1
                except (ValueError, KeyError, TypeError) as error:
                    print(f"Skipping row {row_number}: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def choose_discount(order: Order) -> None:
    print("Discount: 1. None  2. 10%  3. Bulk ($20 off $200+)  4. Student (5%)")
    choice = input("Choose discount (1-4): ").strip()
    options = {"1": NoDiscount(), "2": PercentageDiscount(10),
               "3": BulkDiscount(200, 20), "4": StudentDiscount()}
    order.set_discount(options.get(choice, NoDiscount()))


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
            if price <= 0:
                print("Price must be greater than zero.")
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
        product: Product = ProductFactory.create("physical", product_id, name, price, stock, supplier, weight=weight)
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
        product = ProductFactory.create("digital", product_id, name, price, stock, supplier, download_size=download_size)

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
    print("\n--- Create Order ---")
    inventory.display_all()
    print("Enter a product ID or name to add it to the order.")
    print("Press Enter without typing anything to finish the order.")
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
        print("Line added. Current order:")
        order.display_information()

    if len(order.get_order_lines()) == 0:
        print("Order cancelled (no lines).")
        return
    orders.append(order)
    choose_discount(order)
    order.display_information()


def display_orders_menu(orders: list[Order]):
    if not orders:
        print("No orders have been created yet.")
        return
    print("\n--- Orders ---")
    for order in orders:
        order.display_information()
        print("-" * 30)


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
        print("9. Display orders")
        print("10. Save data")
        print("11. Load products from CSV")
        print("12. Exit")
        print("----------------------------")
        choice = input("\nEnter Option (1-12): ").strip()

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
            display_orders_menu(orders)
        elif choice == "10":
            save_data(inventory, suppliers)
        elif choice == "11":
            if not suppliers:
                print("Add a supplier first (option 6).")
            else:
                display_suppliers_menu(suppliers)
                supplier = find_supplier(suppliers, input("Supplier ID for CSV products: ").strip())
                if supplier is None:
                    print("Supplier not found.")
                else:
                    load_products(input("CSV filename [products.csv]: ").strip() or "products.csv", inventory, supplier)
        elif choice == "12":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-12.")


if __name__ == "__main__":
    main()
