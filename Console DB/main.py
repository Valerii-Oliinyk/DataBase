import json
import os

customers = []
customers_file = ""

def get_customers_file_path():
    return os.path.join(os.path.dirname(__file__), "customers.json")

def get_customers():
    if os.path.exists(customers_file):
        with open(customers_file, "r") as file:
            try:
                data = json.load(file)
                if isinstance(data, list):
                    customers = data
                else:
                    customers = []
            except json.JSONDecodeError:
                customers = []
        return customers

def create():
    Customer = {
        "ID": 0,
        "Name": "",
        "Surname": "",
        "Email": "",
        "DateOfBirth": "",
        "Country": "",
        "IsMember": False,
        "TotalPurchases": 0.0,
        "ActiveDiscount": 0
    }

    Customer["ID"] = len(customers) + 1
    Customer["Name"] = input("Enter Name: ")
    Customer["Surname"] = input("Enter Surname: ")
    Customer["Email"] = input("Enter Email: ")
    Customer["DateOfBirth"] = input("Enter Date of Birth (DD.MM.YYYY): ")
    Customer["Country"] = input("Enter Country: ")
    Customer["IsMember"] = True if input("Is Member (yes/no): ").lower() == "yes" else False
    TotalPurchases = input("Enter Total Purchases: ")
    try:
        TotalPurchases = float(TotalPurchases)
    except ValueError:
        TotalPurchases = 0.0
    ActiveDiscount = input("Enter Active Discount (%): ")
    try:
        ActiveDiscount = int(ActiveDiscount)
    except ValueError:
        ActiveDiscount = 0
    Customer["TotalPurchases"] = TotalPurchases
    Customer["ActiveDiscount"] = ActiveDiscount

    customers.append(Customer)

    clear_console()
    print("Customer created successfully!")
    menu()

def update():
    with open(customers_file, "w") as file:
        json.dump(customers, file, indent=4)
    get_customers()
    clear_console()
    print("Everything updated!")
    menu()

def delete():
    customer_to_delete = input("Enter the ID of the customer to delete: ")
    try:
        customer_to_delete = int(customer_to_delete)
    except ValueError:
        clear_console()
        print("Invalid ID. Please try again.")
        delete()
        return

    if customer_to_delete < 1 or customer_to_delete > len(customers):
        clear_console()
        print("Invalid ID. Please try again.")
        delete()
        return

    customers.pop(customer_to_delete - 1)
    print("Customer deleted successfully!")
    menu()

def get():
    from_customer = int(input("Enter the margin of customers to retrieve:\nFrom:"))
    to_customer = input("To (leave empty for all): ")
    
    if to_customer == "":
        to_customer = len(customers)
    else:
        to_customer = int(to_customer)

    if from_customer < 1:
        clear_console()
        print("Invalid range. The minimal value is 1. Please try again.")
        get()
        return
    if from_customer > to_customer:
        clear_console()
        print("Invalid range. The 'From' value cannot be greater than the 'To' value. Please try again.")
        get()
        return
    if from_customer > len(customers):
        clear_console()
        print("Invalid range. The 'From' value cannot be greater than the total number of customers. Please try again.")
        get()
        return

    if to_customer > len(customers):
        to_customer = len(customers)
        print(f"The right margin of customers is greater than amount of customers.\nMargin set to last customer:{len(customers)}\n")

    for customer in customers[from_customer-1:to_customer]:
        print(customer, "\n")

    clear_console()
    menu()

def menu():
    print("""
        Please select the action:
        1. Create
        2. Update
        3. Delete
        4. Get\n""")

    action = input("Enter the action number: ")

    if action == "1":
        clear_console()
        message("create")
        create()
    elif action == "2":
        clear_console()
        message("update")
        update()
    elif action == "3":
        clear_console()
        message("delete")
        delete()
    elif action == "4":
        clear_console()
        message("get")
        get()
    else:
        clear_console()
        print("Invalid action. Please try again.")
        menu()

def message(ID_of_message):
    if ID_of_message == "create":
        print("\n\nBy using this function, new customer will be created but NOT saved.\nTo save all changes you will need to run the 'Update' function.\n")
        print("""
        1. Continue
        2. Exit to menu
        """)
        action = input("Enter the action number: ")
        if action == "2":
            clear_console()
            menu()
            return
        elif action != "1":
            clear_console()
            print("Invalid action. Please try again.")
            create()
            return
    elif ID_of_message == "update":
        print("\n\nBy using this function, every changes will be saved.\n")
        print("""
        1. Continue
        2. Exit to menu
        """)
        action = input("Enter the action number: ")
        if action == "2":
            clear_console()
            menu()
            return
        elif action != "1":
            clear_console()
            print("Invalid action. Please try again.")
            update()
            return
    elif ID_of_message == "delete":
        print("\n\nBy using this function, selected customer will be deleted, but this action will NOT be saved.\nTo save all changes you will need to run the 'Update' function.\n")
        print("""
        1. Continue
        2. Exit to menu
        """)
        action = input("Enter the action number: ")
        if action == "2":
            clear_console()
            menu()
            return
        elif action != "1":
            clear_console()
            print("Invalid action. Please try again.")
            delete()
            return
    elif ID_of_message == "get":
        print("\n\nBy using this function, all selected customers will be displayed.\n")
        print("""
        1. Continue
        2. Exit to menu
        """)
        action = input("Enter the action number: ")
        if action == "2":
            clear_console()
            menu()
            return
        elif action != "1":
            clear_console()
            print("Invalid action. Please try again.")
            get()
            return

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# OnStart code
customers_file = get_customers_file_path()
customers = get_customers()
print("Welcome to the Console Database!")
menu()