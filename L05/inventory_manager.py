import json
import os

inventory_file = "inventory.json"

def load_inventory():
    if os.path.exists(inventory_file):
        with open(inventory_file, 'r') as file:
            print("inventory.json found")
            return json.load(file)
    return []

def save_inventory(inventory):
    with open(inventory_file, 'w') as file:
        json.dump(inventory, file, indent=4)
    
    
def display_all(inventory):
    if not inventory:
        print("No inventory items found.")
        print()
        return
    else:
        print()
        print("Current Inventory")
        print("-" * 50)
        for item in inventory:
            print(f"ID: {item['id']}| Name: {item['name']}| Price: ${item['price']:.2f}| Stock: {item['stock']}")
        print("-" * 50)
        
def add_product(inventory):
    print()
    print("Add New Product")
    product_id = input("Product ID: ")
    product_name = input("Product Name: ")
    product_price = float(input("Price: "))
    product_stock = int(input("Stock Quantity: "))
    
    new_product = {
        "id": product_id,
        "name": product_name,
        "price": product_price,
        "stock": product_stock
    } 
    inventory.append(new_product)
    save_inventory(inventory)     
    print("Product added successfully!")
    print()  
    
def update_stock(inventory):
    print()
    print("Update Product Stock")
    product_id = input("Enter Product ID: ")
    
    for item in inventory:
        if item['id'] == product_id:
            print("Product Found:")
            print(f"Name: {item['name']} \n Current Stock: {item['stock']}\n")
            new_stock = int(input("New Stock Quantity: "))
            item['stock'] = new_stock
            save_inventory(inventory)
            print(f"Stock updated successfully!")
            print()
            return
    
    print("Product ID not found. Please try again.") 
    
def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ")
    for item in inventory:
        if item['id'] == product_id:
            print("\nProduct Found")
            print("-" * 50)
            print(f"ID: {item['id']}\nName: {item['name']}\nPrice: ${item['price']:.2f}\nStock: {item['stock']}")
            print("-" * 50)
            print()
            return
    print("Product not found.")
        
def main_menu():
    inventory = load_inventory()
    print("=" * 50)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50)

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")
        print()
        
        choice = input("Enter option: ")
        
        if choice == '1':
            display_all(inventory)
        elif choice == '2':
            add_product(inventory)
        elif choice == '3':
            update_stock(inventory)
        elif choice == '4':
            search_product(inventory)
        elif choice == '5':
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json")
        elif choice == '6':
            save_inventory(inventory)
            print("Saving inventory before exit... \nInventory saved successfully.\n")
            print("Thank you for using Inventory Management System. \nProgram terminated.")
            break
        else:
            print("Invalid choice. Please try again.")
            
main_menu()