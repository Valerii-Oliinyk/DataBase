import json
import os
import asyncio
import aiofiles

class StorageBase:
    def Create(self, customer):
        raise NotImplementedError

    def Update(self, customer_id, updated_fields):
        raise NotImplementedError

    def Delete(self, customer_id):
        raise NotImplementedError

    def Get(self):
        raise NotImplementedError

    def SaveChanges(self):
        raise NotImplementedError

class InMemory(StorageBase):
    def __init__(self):
        self.customers = []

    def Create(self, customer):
        self.customers.append(customer)

    def Update(self, customer_id, updated_fields):
        for customer in self.customers:
            if customer["ID"] == customer_id:
                customer.update(updated_fields)
                return True
        return False

    def Delete(self, customer_id):
        self.customers = [c for c in self.customers if c["ID"] != customer_id]

    def Get(self):
        return self.customers

    def SaveChanges(self):
        pass  # No action needed for in-memory

class JSONStorage(StorageBase):
    def __init__(self, file_path):
        self.file_path = file_path
        self.customers = asyncio.run(self._load_async())

    async def _load_async(self):
        if os.path.exists(self.file_path):
            async with aiofiles.open(self.file_path, "r", encoding="utf-8") as file:
                try:
                    content = await file.read()
                    data = json.loads(content)
                    if isinstance(data, list):
                        return data
                except (json.JSONDecodeError, FileNotFoundError):
                    pass
        return []

    def Create(self, customer):
        self.customers.append(customer)

    def Update(self, customer_id, updated_fields):
        for customer in self.customers:
            if customer["ID"] == customer_id:
                customer.update(updated_fields)
                return True
        return False

    def Delete(self, customer_id):
        self.customers = [c for c in self.customers if c["ID"] != customer_id]

    def Get(self):
        return self.customers

    def SaveChanges(self):
        asyncio.run(self._save_async())

    async def _save_async(self):
        async with aiofiles.open(self.file_path, "w", encoding="utf-8") as file:
            await file.write(json.dumps(self.customers, indent=4))

def get_customers_file_path():
    return os.path.join(os.path.dirname(__file__), "customers.json")

def select_storage():
    print("Select storage type:")
    print("1. InMemory")
    print("2. JSON")
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        return InMemory()
    elif choice == "2":
        return JSONStorage(get_customers_file_path())
    else:
        print("Invalid choice. Defaulting to InMemory.")
        return InMemory()

storage = select_storage()

def create():
    Customer = {
        "ID": len(storage.Get()) + 1,
        "Name": input("Enter Name: "),
        "Surname": input("Enter Surname: "),
        "Email": input("Enter Email: "),
        "DateOfBirth": input("Enter Date of Birth (DD.MM.YYYY): "),
        "Country": input("Enter Country: "),
        "IsMember": True if input("Is Member (yes/no): ").lower() == "yes" else False,
        "TotalPurchases": 0.0,
        "ActiveDiscount": 0
    }
    try:
        Customer["TotalPurchases"] = float(input("Enter Total Purchases: "))
    except ValueError:
        Customer["TotalPurchases"] = 0.0
    try:
        Customer["ActiveDiscount"] = int(input("Enter Active Discount (%): "))
    except ValueError:
        Customer["ActiveDiscount"] = 0

    storage.Create(Customer)
    clear_console()
    print("Customer created successfully!")
    menu()

def SaveChanges():
    storage.SaveChanges()
    clear_console()
    print("Everything updated!")
    menu()

def Update():
    customers = storage.Get()
    customer_id = input("Enter the ID of the customer to update: ")
    try:
        customer_id = int(customer_id)
    except ValueError:
        clear_console()
        print("Invalid ID. Please try again.")
        Update()
        return

    customer = next((c for c in customers if c["ID"] == customer_id), None)
    if not customer:
        clear_console()
        print("Customer not found. Please try again.")
        Update()
        return

    print("Current customer data:", customer)
    fields = ["Name", "Surname", "Email", "DateOfBirth", "Country", "IsMember", "TotalPurchases", "ActiveDiscount"]
    updated_fields = {}
    for field in fields:
        value = input(f"Enter new value for {field} (leave empty to keep current): ")
        if value != "":
            if field == "IsMember":
                updated_fields[field] = True if value.lower() == "yes" else False
            elif field == "TotalPurchases":
                try:
                    updated_fields[field] = float(value)
                except ValueError:
                    continue
            elif field == "ActiveDiscount":
                try:
                    updated_fields[field] = int(value)
                except ValueError:
                    continue
            else:
                updated_fields[field] = value
    storage.Update(customer_id, updated_fields)
    clear_console()
    print("Customer updated successfully!")
    menu()

def delete():
    customer_id = input("Enter the ID of the customer to delete: ")
    try:
        customer_id = int(customer_id)
    except ValueError:
        clear_console()
        print("Invalid ID. Please try again.")
        delete()
        return

    storage.Delete(customer_id)
    print("Customer deleted successfully!")
    menu()

def get():
    customers = storage.Get()
    from_customer = int(input("Enter the margin of customers to retrieve:\nFrom:"))
    to_customer = input("To (leave empty for all): ")
    if to_customer == "":
        to_customer = len(customers)
    else:
        to_customer = int(to_customer)
    if from_customer < 1 or from_customer > to_customer or from_customer > len(customers):
        clear_console()
        print("Invalid range. Please try again.")
        get()
        return
    if to_customer > len(customers):
        to_customer = len(customers)
        print(f"Margin set to last customer: {len(customers)}\n")
    for customer in customers[from_customer-1:to_customer]:
        print(customer, "\n")
    clear_console()
    menu()

def menu():
    print("""
        Please select the action:
        1. Create
        2. SaveChanges
        3. Delete
        4. Get
        5. Update\n""")
    action = input("Enter the action number: ")
    if action == "1":
        clear_console()
        message("create")
        create()
    elif action == "2":
        clear_console()
        message("savechanges")
        SaveChanges()
    elif action == "3":
        clear_console()
        message("delete")
        delete()
    elif action == "4":
        clear_console()
        message("get")
        get()
    elif action == "5":
        clear_console()
        message("update")
        Update()
    else:
        clear_console()
        print("Invalid action. Please try again.")
        menu()

def message(ID_of_message):
    if ID_of_message == "create":
        print("\n\nBy using this function, new customer will be created but NOT saved.\nTo save all changes you will need to run the 'SaveChanges' function.\n")
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
    elif ID_of_message == "savechanges":
        print("\n\nBy using this function, every change will be saved.\n")
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
            SaveChanges()
            return
    elif ID_of_message == "delete":
        print("\n\nBy using this function, selected customer will be deleted, but this action will NOT be saved.\nTo save all changes you will need to run the 'SaveChanges' function.\n")
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
    elif ID_of_message == "update":
        print("\n\nBy using this function, you can update customer data.\n")
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
            Update()
            return

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

print("Welcome to the Console Database!")
menu()