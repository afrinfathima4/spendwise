
import json
from models import Expense


def save_to_json(filename, expenses_list):
    data = []

    for expense in expenses_list:
        data.append(expense.to_dict())

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Expenses saved successfully.")

    except OSError as error:
        print("Error saving expenses:", error)


def load_from_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Invalid JSON data. Starting with an empty list.")
            return []

        expenses = []

        for item in data:
            try:
                expense = Expense.from_dict(item)
                expenses.append(expense)

            except (KeyError, TypeError, ValueError) as error:
                print("Skipping invalid expense record:", error)

        return expenses

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("JSON file is empty or corrupted. Starting with an empty list.")
        return []

    except OSError as error:
        print("Error loading expenses:", error)
        return []
