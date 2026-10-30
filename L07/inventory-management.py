import json
from inventory import Inventory

FILENAME = "inventory.json"


def title_display():
    print("=" * 50)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50)


def load_inventory(inventory):
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
        for item in data:
            inventory.add_product(
                item["name"], item["price"], item["stock"], item["product_id"]
            )

        print(f"Loaded {len(data)} product(s) from {FILENAME}.")
    except FileNotFoundError:
        print("No saved inventory found. Starting with an empty inventory.")
    except (json.JSONDecodeError, KeyError):
        print("Saved inventory file is damaged. Starting with an empty inventory.")


def save_inventory(inventory):
    data = [product.product_dict() for product in inventory.get_products()]
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Inventory saved to {FILENAME}.")


def add_product_menu(inventory):
    while True:
        name = input("Product Name: ").strip()
        if name == "":
            print("Name cannot be empty.")
        else:
            break

    while True:
        try:
            price = float(input("Price: "))
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

    product = inventory.add_product(name, price, stock)
    if product is not None:
        print(f"Product added with ID {product.get_product_id()}.")


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
    term = input("Enter product ID or Name: ").strip()
    product = inventory.search_product(term)
    if product is None:
        print("Product not found.")
    else:
        product.display_information()


def main():
    inventory = Inventory()
    load_inventory(inventory)
    
    title_display()

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
