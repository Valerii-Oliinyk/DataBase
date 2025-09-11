import json
import os

customers = []
customers_file = ""

def get_customers_file_path():
    return os.path.join(os.path.dirname(__file__), "customers.json")
    

def get_customers(customers):
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

def create(customers):
    Customer = {
        "Name": "",
        "Surname": "",
        "Email": "",
        "DateOfBirth": "",
        "Country": "",
        "IsMember": False,
        "TotalPurchases": 0.0,
        "ActiveDiscount": 0
    }

    Customer["Name"] = input("Enter Name: ")
    Customer["Surname"] = input("Enter Surname: ")
    Customer["Email"] = input("Enter Email: ")
    Customer["DateOfBirth"] = input("Enter Date of Birth (DD.MM.YYYY): ")
    Customer["Country"] = input("Enter Country: ")
    Customer["IsMember"] = True if input("Is Member (yes/no): ").lower() == "yes" else False
    Customer["TotalPurchases"] = float(input("Enter Total Purchases: "))
    Customer["ActiveDiscount"] = int(input("Enter Active Discount (%): "))

    customers.append(Customer)

    print("Customer created successfully!")
    menu()

def update():
    with open(customers_file, "w") as file:
        json.dump(customers, file, indent=4)
    get_customers(customers)
    menu()

def delete():
    pass

def get():
    pass

def menu():
    print("""
        Please select the action:
        1. Create
        2. Update
        3. Delete
        4. Get\n""")

    action = input("Enter the action number: ")

    if action == "1":
        create(customers)
    elif action == "2":
        update()
    elif action == "3":
        delete()
    elif action == "4":
        get()
    else:
        print("Invalid action. Please try again.")
        menu()


# OnStart code
customers_file = get_customers_file_path()
get_customers(customers)
print("Welcome to the Console Database!")
menu()