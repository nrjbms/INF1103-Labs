import json
from inventory import Inventory
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct

FILENAME = "inventory.json"


def title_display():
    print("=" * 50)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50)


def create_product_from_dict(item):
    if item["type"] == "physical":
        return PhysicalProduct(item["product_id"],item["name"],item["price"],item["stock"],item["weight"],)
    if item["type"] == "digital":
        return DigitalProduct( item["product_id"],item["name"],item["price"],item["stock"],item["download_size"],)
    raise ValueError(f"Unknown product type: {item['type']}")


def load_inventory(inventory):
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
        products = [create_product_from_dict(item) for item in data]
        for product in products:
            inventory.add_product(product)
        print(f"Loaded {len(products)} product(s) from {FILENAME}.")
    except FileNotFoundError:
        print("No saved inventory found. Starting with an empty inventory.")
    except (json.JSONDecodeError, KeyError, ValueError):
        print("Saved inventory file is damaged. Starting with an empty inventory.")


def save_inventory(inventory):
    data = [product.product_dict() for product in inventory.get_products()]
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Inventory saved to {FILENAME}.")


def add_product_menu(inventory):
    while True:
        print("Product Type:")
        print("  1. Physical product")
        print("  2. Digital product")
        type_choice = input("Choose type (1-2): ").strip()
        if type_choice in ("1", "2"):
            break
        print("Please enter 1 or 2.")

    while True:
        name = input("Product Name: ").strip()
        if name == "":
            print("Name cannot be empty.")
        else:
            break

    while True:
        try:
            price = float(input("Enter Price: "))
            if price < 0:
                print("Price cannot be negative.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            stock = int(input("Stock Quantity: "))
            if stock < 0:
                print("Stock cannot be negative.")
            else:
                break
        except ValueError:
            print("Please enter a whole number.") 


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
                
        product_id = inventory.generate_id() 
        product = PhysicalProduct(product_id, name, price, stock, weight)
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
        product_id = inventory.generate_id() 
        product = DigitalProduct(product_id, name, price, stock, download_size)

    if inventory.add_product(product):
        print(f"Product added with ID {product_id}.")


def update_stock_menu(inventory):
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


def search_product_menu(inventory):
    term = input("Enter product ID or name: ").strip()
    product = inventory.search_product(term)
    if product is None:
        print("Product not found.")
    else:
        product.display_information()
        print(f"    Fulfilment: {product.get_fulfilment_info()}")


def main():
    title_display()
    inventory = Inventory()
    load_inventory(inventory)

    while True:
        print("\n----------- MENU -----------")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")
        print("----------------------------")
        choice = input("\nEnter Option (1-6): ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_menu(inventory)
        elif choice == "3":
            update_stock_menu(inventory)
        elif choice == "4":
            search_product_menu(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-6.")


main()
