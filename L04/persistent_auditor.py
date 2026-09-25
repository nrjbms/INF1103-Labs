inventory = "order.txt"

    

def load_inventory():
    orders = []
    
    open(inventory, 'a').close()
    file = open(inventory, 'r')
    for line in file:
        order_id, product, quantity = line.strip().split(',')
        orders.append([order_id.strip(), product.strip(), quantity.strip()])
    file.close()
    return orders


def save_inventory(orders):
    file = open(inventory, 'w')
    for order in orders:
        file.write(order[0] + "," + order[1] + "," + order[2] + "\n")
    file.close()


def get_valid_input():
    while True:
        print ("Type 'quit' to exit the program.")
        product_input = input("Enter Product Name: ")
        if product_input.lower() == 'quit':
            return "quit"
        
        quantity_input = input("Enter Quantity: ")
        if quantity_input.lower() == 'quit':
            return "quit"
        
        if quantity_input.isdigit() == False or int(quantity_input) == 0:
            print("Invalid input. Please enter a valid quantity.")
            continue

        return product_input, int(quantity_input)

def generate_report(orders):
    print("Current Orders: ")
    print()
    for order in orders:
        print(order[0] + ", " + order[1] + ", " + order[2])
    print()

orders = load_inventory()
generate_report(orders)

while True:
    result = get_valid_input()

    if result == "quit":
        generate_report(orders)
        break

    product, quantity = result

    if len(orders) == 0:
        new_id = 1001
    else:
        new_id = int(orders[-1][0]) + 1

    new_order = [str(new_id), product, str(quantity)]
    orders.append(new_order)

    print()
    print("New Order Added:")
    print(new_order[0] + ", " + new_order[1] + ", " + new_order[2])
    print()

save_inventory(orders)
print("Order successfully saved to order.txt")

    