
from models import Expense, ExpenseTracker
from storage import save_to_json, load_from_json
from utils import (
    is_valid_date,
    parse_tags,
    generate_expense_id,
    InvalidInputError
)


FILENAME = "expenses.json"


def add_expense(tracker):
    date = input("Enter date (YYYY-MM-DD): ").strip()

    if not is_valid_date(date):
        print("Invalid date! Please use YYYY-MM-DD.")
        return

    category = input("Enter category: ").strip().title()

    if category == "":
        print("Category cannot be empty.")
        return

    try:
        amount = float(input("Enter amount: ₹"))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Invalid amount! Please enter a number.")
        return

    tag_text = input("Enter tags separated by commas: ")
    tags = parse_tags(tag_text)

    try:
        expense_id = generate_expense_id(tracker.expenses)
    except InvalidInputError as error:
        print("Error:", error)
        return

    expense = Expense(
        expense_id,
        date,
        category,
        amount,
        tags
    )

    tracker.add_expense(expense)

    print("\nExpense added successfully!")
    print(expense)

    show_budget_status(tracker)


def view_expenses(tracker):
    if len(tracker.expenses) == 0:
        print("\nNo expenses available.")
        return

    print("\n" + "-" * 75)
    print(f"{'ID':<10} {'DATE':<14} {'CATEGORY':<18} {'AMOUNT':>12}  TAGS")
    print("-" * 75)

    sorted_expenses = tracker.sort_by_amount()

    for expense in sorted_expenses:
        tags = ", ".join(sorted(expense.tags)) if expense.tags else "none"

        print(
            f"{expense.expense_id:<10} "
            f"{expense.date:<14} "
            f"{expense.category:<18} "
            f"₹{expense.amount:>10.2f}  "
            f"{tags}"
        )

    print("-" * 75)
    show_budget_status(tracker)


def show_category_summary(tracker):
    summary = tracker.get_category_summary()

    if len(summary) == 0:
        print("\nNo expenses available for summary.")
        return

    print("\n--- Category Summary ---")

    for category, total in summary.items():
        print(f"{category}: ₹{total:.2f}")

    count, total = tracker.get_summary_data()

    print("\nTotal number of expenses:", count)
    print(f"Total spending: ₹{total:.2f}")


def search_by_category(tracker):
    category = input("Enter category to search: ").strip()

    if category == "":
        print("Category cannot be empty.")
        return

    results = tracker.filter_by_category(category)

    if len(results) == 0:
        print("No expenses found in this category.")
    else:
        print("\nExpenses found:")

        for expense in results:
            print(expense)


def show_budget_status(tracker):
    total = tracker.get_total_spending()
    budget = tracker.budget_limit

    print(f"\nTotal spending: ₹{total:.2f}")
    print(f"Budget limit: ₹{budget:.2f}")
    print(f"Remaining budget: ₹{budget - total:.2f}")

    if tracker.is_over_budget():
        print("Warning! You have exceeded your budget.")
    elif budget > 0 and total >= budget * 0.8:
        print("Warning! You are approaching your budget limit.")
    else:
        print("You are within your budget.")


def main():
    expenses = load_from_json(FILENAME)

    try:
        budget = float(input("Enter your budget limit: ₹"))

        if budget <= 0:
            print("Budget must be greater than zero. Using ₹5000.")
            budget = 5000.0

    except ValueError:
        print("Invalid budget. Using ₹5000.")
        budget = 5000.0

    tracker = ExpenseTracker(budget, expenses)

    print("\nWelcome to SpendWise CLI!")
    print("Loaded expenses:", len(tracker.expenses))

    while True:
        print("\n========== SPENDWISE ==========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Category Summary")
        print("4. Search Expenses by Category")
        print("5. Save and Exit")
        print("================================")

        choice = input("Enter your choice: ").strip().lower()

        match choice:
            case "1":
                add_expense(tracker)

            case "2":
                view_expenses(tracker)

            case "3":
                show_category_summary(tracker)

            case "4":
                search_by_category(tracker)

            case "5" | "exit":
                save_to_json(FILENAME, tracker.expenses)
                print("Thank you for using SpendWise!")
                break

            case _:
                print("Invalid option! Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
