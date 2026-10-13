
import re
from datetime import datetime


class InvalidInputError(Exception):
    pass


def is_valid_date(date_text):
    pattern = r"^\d{4}-\d{2}-\d{2}$"

    if not re.fullmatch(pattern, date_text):
        return False

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_expense_id(expense_id):
    pattern = r"EXP-[0-9]{3}"
    return re.fullmatch(pattern, expense_id) is not None


def parse_tags(tag_text):
    tags = tag_text.strip().lower().split(",")

    result = set()

    for tag in tags:
        tag = tag.strip()

        if tag != "":
            result.add(tag)

    return result


def generate_expense_id(expenses):
    highest_id = 0

    for expense in expenses:
        match = re.fullmatch(r"EXP-(\d{3})", expense.expense_id)

        if match:
            number = int(match.group(1))

            if number > highest_id:
                highest_id = number

    if highest_id >= 999:
        raise InvalidInputError("Maximum expense ID limit reached.")

    return f"EXP-{highest_id + 1:03d}"
