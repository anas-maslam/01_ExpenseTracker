import datetime
import json
import os.path
from datetime import datetime


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __str__(self):
        return f"{self.name} - {self.email}"

    def login(self, email, password):
        if not os.path.exists("user.json"):
            return ""
        with open("user.json", "r") as file:
            users = json.load(file)
            for user in users:
                if user["email"] == email and user["password"] == password:
                    return user["email"]
        return ""

    def add_user(self, name, email, password):
        user = User(name, email, password)
        return user

    def delete_user(self, email):
        with open("user.json", "r") as file:
            users = json.load(file)
        if self.email == email:
            del self.email
        else:
            print("Invalid email")

    def view_user(self):
        return self.name, self.email

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    def append_user_json_file(self, name, email, password):
        users = []
        if os.path.exists("user.json"):
            with open("user.json", "r") as file:
                users = json.load(file)
        user = self.add_user(name, email, password)
        users.append(user.to_dict())
        with open("user.json", "w") as file:
            json.dump(users, file, indent=4)

    @staticmethod
    def print_all_users():
        with open("user.json", "r") as file:
            users = json.load(file)
            for user in users:
                print(user)


class Expense:
    def __init__(self, sno, amount, category, description="", date=""):
        self.sno = sno
        self.amount = amount
        self.category = category
        self.description = description
        if date == "":
            from datetime import date
            self.date = date.today().strftime("%Y-%m-%d")
        else:
            self.date = date
        # self.date = date or date.today().strftime("%Y-%m-%d")

    def __str__(self):
        return f"{self.sno} - {self.category}: {self.amount} - {self.description} on {self.date}"

    def to_dict(self):
        return {
            "sno": self.sno,
            "description": self.description,
            "category": self.category,
            "amount": self.amount,
            "date": self.date
        }


class ExpenseTracker:
    def __init__(self):
        self.expenses = {}

    def add_expense(self, email, sno, amount, category, description="", date=None):
        if amount <= 0:
            print("Invalid amount")
            return
        if not category:
            print("Category is required")
            return
        if not description:
            print("Description is required")
            return
        expense = Expense(sno, amount, category, description, date)

        # if not email in self.expenses:
        #     self.expenses[email] = []
        # # if not self.expenses[email]:
        # #     self.expenses[email] = []
        # self.expenses[email].append(expense)
        return expense

    def delete_expense(self, sno, email):
        if email in self.expenses:
            expenses_for_email = self.expenses[email]  # Accessing the list using the __getitem__ method

            for expense in expenses_for_email:
                if int(expense["sno"]) == sno:
                    print(f"Deleting expense {sno} for {email}.")
                    # Remove the expense from the list of expenses
                    self.expenses[email] = [t for t in expenses_for_email if t["sno"] != sno]
                    self.save_expenses()
                    return True
        return False

    def save_expenses(self):
        with open("expenses.json", "w") as file:
            json.dump(self.expenses, file, indent=4)

    def view_expenses(self, email):
        if os.path.exists("expenses.json"):
            with open("expenses.json", "r") as file:
                try:
                    existing_expenses = json.load(file)
                    self.expenses = existing_expenses
                except json.JSONDecodeError:
                    self.expenses = {}

        else:
            self.expenses = {}

        # Display the user's expenses
        if not self.expenses[email]:
            print("No expenses found for this user.")
        else:
            print("Expenses for:", email)
            for expense in self.expenses[email]:
                print(expense)

        # if not email in self.expenses:
        #     self.expenses[email] = []
        # else:
        #     # Load expenses for the given email if they exist in the JSON
        #     if email in existing_expenses:
        #         self.expenses[email] = [
        #             Expense(
        #                 expense["sno"],
        #                 expense["amount"],
        #                 expense["category"],
        #                 expense["description"],
        #                 datetime.datetime.strptime(expense["date"], "%Y-%m-%d").date()
        #             ) for expense in existing_expenses[email]
        #         ]
        #     else:
        #         # If there are no expenses for this email, you can initialize it
        #         self.expenses[email] = []  # Ensure it's initialized
        #
        #     # Display the user's expenses
        #     if not self.expenses[email]:
        #         print("No expenses found for this user.")
        #     else:
        #         print("Expenses for:", email)
        #         for expense in self.expenses[email]:
        #             print(expense)

    def total_expenses(self, email):
        return sum(expense["amount"] for expense in self.expenses[email])

    def filter_by_category(self, email, category):
        return [expense for expense in self.expenses[email] if expense["category"] == category]

    def monthly_report(self, email, month, year):
        # Open to debug
        # if email in self.expenses:
        #     for expense in self.expenses[email]:
        #         print(datetime.strptime(expense["date"], "%Y-%m-%d").strftime("%m"), datetime.strptime(expense["date"], "%Y-%m-%d").strftime("%Y"))

        if email in self.expenses:
            report = [expense for expense in self.expenses[email]
                      if int(datetime.strptime(expense["date"], "%Y-%m-%d").strftime("%m")) == month and
                      int(datetime.strptime(expense["date"], "%Y-%m-%d").strftime("%Y")) == year]
            return report
        else:
            print(f"No expenses found for \"{email}\" user for \"{month}-{year}\".")
            return []

    def search_expenses(self, email, keyword):
        return [expense for expense in self.expenses[email] if keyword.lower() in expense["description"].lower()]

    def write_expenses_json_file(self, email, expense):
        if os.path.exists("expenses.json"):
            with open("expenses.json", "r") as file:
                try:
                    existing_expenses = json.load(file)
                except json.JSONDecodeError:
                    existing_expenses = {}
        else:
            existing_expenses = {}
        if not email in existing_expenses:
            existing_expenses[email] = []

        # existing_expenses[email].extend([expense.to_dict() for expense in self.expenses[email]])
        existing_expenses[email].extend([expense.to_dict()])
        # existing_expenses[email].append([expense.to_dict() for expense in self.expenses[email]])
        with open("expenses.json", "w") as file:
            json.dump(existing_expenses, file, indent=4)

    def read_all_expenses_json_file(self, email):
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
            return [Expense(expense["amount"], expense["category"], expense["description"], datetime.datetime.strptime(expense["date"], "%Y-%m-%d").date()) for expense in expenses[email]]

    def load_expenses(self, email):
        if os.path.exists("expenses.json"):
            with open("expenses.json", "r") as file:
                try:
                    existing_expenses = json.load(file)
                    self.expenses = existing_expenses
                except json.JSONDecodeError:
                    self.expenses = {}
        else:
            self.expenses = {}


def expense_tracker_menu():
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Login")
        print("2. Register")
        print("3. View Users")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            email = input("Enter email: ")
            password = input("Enter password: ")
            user = User("", email, password)
            authenticated_username = user.login(email, password)
            if authenticated_username != "":
                print(f"Welcome \"{authenticated_username}\": Login successful...")
                break
            else:
                print("Login failed. Please try again.\n")

        if choice == "2":
            name = input("Enter name: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            user = User(name, email, password)
            user.append_user_json_file(name, email, password)

        if choice == "3":
            User.print_all_users()

        if choice == "4":
            break

    tracker = ExpenseTracker()
    tracker.load_expenses(email)

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. Delete Expense")
        print("3. View Expenses")
        print("4. Filter by Category")
        print("5. Monthly Report")
        print("6. Search Expenses")
        print("7. Total Expenses")
        print("8. Exit\n")
        choice = input("Enter your choice: ")

        if choice == "1":
            def get_max_sno_json_file(email):
                if not os.path.exists("expenses.json"):
                    return 0
                with open("expenses.json", "r") as file:
                    expenses = json.load(file)
                    if not email in expenses:
                        return 0
                    return max(expense["sno"] for expense in expenses[email])

            sno = get_max_sno_json_file(email) + 1
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            date = datetime.datetime.strptime(date_input, "%Y-%m-%d") if date_input else ""
            # date = date_input if date_input else None
            expense = tracker.add_expense(email, sno, amount, category, description, date)
            tracker.write_expenses_json_file(email, expense)

        elif choice == "2":
            tracker.view_expenses(email)
            sno = int(input("\n\nEnter expense sno to delete: "))
            tracker.delete_expense(sno, email)

        elif choice == "3":
            tracker.view_expenses(email)

        elif choice == "4":
            tracker.view_expenses(email)
            category = input("\n\nEnter category to filter by: ")
            filtered = tracker.filter_by_category(email, category)
            for expense in filtered:
                print(expense)

        elif choice == "5":
            month = int(input("Enter month (1-12): "))
            year = int(input("Enter year: "))
            report = tracker.monthly_report(email, month, year)
            for expense in report:
                print(expense)

        elif choice == "6":
            keyword = input("Enter keyword to search expenses: ")
            searched = tracker.search_expenses(email, keyword)
            if not searched:
                print("No expenses found for the given keyword")
            else:
                for expense in searched:
                    print(expense)

        elif choice == "7":
            print(f"Total expenses for \"{email}\" user: {tracker.total_expenses(email)}")

        elif choice == "8":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    expense_tracker_menu()
