inventory = 0
deliveries_processed = 0
failed = 0
total_tax = 0

def get_valid_input():
    failed_attempts = 0
    while True:
        user_input = input("Enter a number (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            return "quit", failed_attempts
        
        if user_input.isdigit() == False:
            print("Invalid input. Please enter a valid number.")
            failed_attempts += 1
            continue

        else:
            return int(user_input), failed_attempts

def process_delivery(current_total, new_value):
    return current_total + new_value  

def calculate_tax(total_units):
    tax_rate = 0.1 
    return total_units * tax_rate    

def generate_report(deliveries_processed, failed_attempts, tax):
    print("Total Deliveries Processed: ", deliveries_processed)
    print("Number of Failed/Rejected Entries: ", failed_attempts)
    print("Total Tax Collected: $", tax)

while True:

    user_input, failed_attempts = get_valid_input()
    failed += failed_attempts

    if user_input == "quit":
        break

    inventory = process_delivery(inventory, user_input)
    total_tax += calculate_tax(user_input)
    deliveries_processed += 1

generate_report(deliveries_processed, failed, total_tax)