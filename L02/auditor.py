
inventory = 0
failed = 0

while True:

    user_input = input("Enter a number (or 'quit' to exit): ")
    if user_input.lower() == 'quit':
        break

    if user_input.isdigit() == False:
        print("Invalid input. Please enter a valid number.")
        failed += 1
        continue

    if int(user_input) < 0 :
        print("Invalid input. Please enter a non-negative number.")
        failed += 1
        continue

    if inventory >= 500:
                print("Inventory limit exceeded.")
                failed += 1
                break

    inventory += int(user_input)
    
    

print("Total Units Processed: ", inventory)
print("Number of Failed/Rejected Entries: ",failed)
