import csv
import os
from datetime import datetime

class PersonalExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.monthly_budget = 0
        self.filename = "expenses.csv"
        self.load_expenses()

    def add_expense(self):
        """Function to add a new expense"""
        print("\n--- Add New Expense ---")

        # Get date input
        while True:
            date_input = input("Enter the date (YYYY-MM-DD): ").strip()
            try:
                # Validate date format
                datetime.strptime(date_input, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD format.")

        # Get category
        category = input("Enter the category (e.g., Food, Travel, Entertainment): ").strip()
        while not category:
            category = input("Category cannot be empty. Please enter a category: ").strip()

        # Get amount
        while True:
            try:
                amount = float(input("Enter the amount spent: $"))
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a valid number.")

        # Get description
        description = input("Enter a brief description: ").strip()
        while not description:
            description = input("Description cannot be empty. Please enter a description: ").strip()

        # Create expense dictionary
        expense = {
            'date': date_input,
            'category': category,
            'amount': amount,
            'description': description
        }

        # Add to expenses list
        self.expenses.append(expense)
        print(f"Expense added successfully! ${amount:.2f} for {category}")

    def view_expenses(self):
        """Function to display all stored expenses"""
        print("\n--- Your Expenses ---")

        if not self.expenses:
            print("No expenses recorded yet.")
            return

        print(f"{'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
        print("-" * 60)

        total = 0
        for expense in self.expenses:
            # Validate that all required fields are present
            if all(key in expense and expense[key] for key in ['date', 'category', 'amount', 'description']):
                print(f"{expense['date']:<12} {expense['category']:<15} ${expense['amount']:<9.2f} {expense['description']}")
                total += expense['amount']
            else:
                print("Incomplete expense entry found - skipping")

        print("-" * 60)
        print(f"Total expenses: ${total:.2f}")

    def set_budget(self):
        """Function to set monthly budget"""
        print("\n--- Set Monthly Budget ---")
        while True:
            try:
                budget = float(input("Enter your monthly budget: $"))
                if budget <= 0:
                    print("Budget must be greater than 0.")
                    continue
                self.monthly_budget = budget
                print(f"Monthly budget set to ${budget:.2f}")
                break
            except ValueError:
                print("Invalid amount. Please enter a valid number.")

    def track_budget(self):
        """Function to track budget and show remaining balance or overspend warning"""
        print("\n--- Budget Tracking ---")

        if self.monthly_budget == 0:
            print("No monthly budget set. Please set a budget first.")
            self.set_budget()
            return

        # Calculate total expenses
        total_expenses = sum(expense['amount'] for expense in self.expenses
                             if all(key in expense and expense[key] for key in ['date', 'category', 'amount', 'description']))

        print(f"Monthly Budget: ${self.monthly_budget:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")

        if total_expenses > self.monthly_budget:
            overspend = total_expenses - self.monthly_budget
            print(f"You have exceeded your budget by ${overspend:.2f}!")
        else:
            remaining = self.monthly_budget - total_expenses
            print(f"You have ${remaining:.2f} left for the month")

    def save_expenses(self):
        """Function to save expenses to CSV file"""
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                if self.expenses:
                    fieldnames = ['date', 'category', 'amount', 'description']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.expenses)

                # Save budget info in a separate line (simple approach)
                file.write(f"#BUDGET,{self.monthly_budget}\n")

            print(f"Expenses saved to {self.filename}")
        except Exception as e:
            print(f"Error saving expenses: {e}")

    def load_expenses(self):
        """Function to load expenses from CSV file"""
        if not os.path.exists(self.filename):
            print(f"No existing expense file found. Starting fresh.")
            return

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                # Read all lines
                lines = file.readlines()

                # Check for budget line
                budget_line = None
                csv_lines = []

                for line in lines:
                    if line.startswith("#BUDGET,"):
                        budget_line = line
                    else:
                        csv_lines.append(line)

                # Load budget if found
                if budget_line:
                    try:
                        self.monthly_budget = float(budget_line.split(',')[1].strip())
                    except (ValueError, IndexError):
                        self.monthly_budget = 0

                # Process CSV data
                if csv_lines:
                    # Write CSV lines to a temporary string for csv.reader
                    csv_content = ''.join(csv_lines)
                    csv_reader = csv.DictReader(csv_content.splitlines())

                    for row in csv_reader:
                        # Validate and convert amount to float
                        try:
                            row['amount'] = float(row['amount'])
                            self.expenses.append(row)
                        except (ValueError, KeyError):
                            print(f"Skipping invalid expense entry: {row}")

            print(f"Loaded {len(self.expenses)} expenses from {self.filename}")
            if self.monthly_budget > 0:
                print(f"Monthly budget: ${self.monthly_budget:.2f}")

        except Exception as e:
            print(f"Error loading expenses: {e}")

    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("         PERSONAL EXPENSE TRACKER")
        print("="*50)
        print("1. Add expense")
        print("2. View expenses")
        print("3. Track budget")
        print("4. Save expenses")
        print("5. Exit")
        print("-"*50)

    def run(self):
        """Main function to run the expense tracker"""
        print("Welcome to Personal Expense Tracker!")

        while True:
            self.display_menu()

            choice = input("Please select an option (1-5): ").strip()

            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.track_budget()
            elif choice == '4':
                self.save_expenses()
            elif choice == '5':
                print("\nSaving expenses and exiting...")
                self.save_expenses()
                print("Thank you for using Personal Expense Tracker!")
                break
            else:
                print("Invalid option. Please select a number between 1 and 5.")

# Run the expense tracker
if __name__ == "__main__":
    tracker = PersonalExpenseTracker()
    tracker.run()