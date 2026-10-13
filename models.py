
class Expense:
    def __init__(self, expense_id, date, category, amount, tags):
        self.expense_id = expense_id
        self.date = date
        self.category = category
        self.amount = float(amount)
        self.tags = set(tags)

    def to_dict(self):
        data = {
            "expense_id": self.expense_id,
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "tags": list(self.tags)
        }
        return data

    @classmethod
    def from_dict(cls, data):
        expense = cls(
            data["expense_id"],
            data["date"],
            data["category"],
            data["amount"],
            data.get("tags", [])
        )
        return expense

    def __str__(self):
        tags_text = ", ".join(sorted(self.tags)) if self.tags else "none"
        return f"[{self.date}] {self.category}: ₹{self.amount:.2f} (tags: {tags_text})"


class ExpenseTracker:
    def __init__(self, budget_limit, expenses=None):
        self.expenses = expenses if expenses is not None else []
        self.budget_limit = float(budget_limit)

    def add_expense(self, expense):
        self.expenses.append(expense)

    def get_total_spending(self):
        total = 0

        for expense in self.expenses:
            total = total + expense.amount

        return total

    def is_over_budget(self):
        total = self.get_total_spending()

        if total > self.budget_limit:
            return True
        else:
            return False

    def get_category_summary(self):
        summary = {}

        for expense in self.expenses:
            category = expense.category

            if category in summary:
                summary[category] = summary[category] + expense.amount
            else:
                summary[category] = expense.amount

        return summary

    def filter_by_category(self, category_name):
        result = []

        for expense in self.expenses:
            if expense.category.lower() == category_name.lower():
                result.append(expense)

        return result

    def get_summary_data(self):
        count = len(self.expenses)
        total = self.get_total_spending()

        return (count, total)

    def sort_by_amount(self):
        sorted_expenses = sorted(
            self.expenses,
            key=lambda expense: expense.amount,
            reverse=True
        )

        return sorted_expenses
