from datetime import datetime
from abc import ABC, abstractmethod

# -----------------------------
# REUSED CORE CLASSES
# -----------------------------
class Vehicle:
    def __init__(self, plate, vtype):
        self.plate = plate
        self.vtype = vtype


class Ticket:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.entry_time = datetime.now()
        self.exit_time = None

    def close_ticket(self):
        self.exit_time = datetime.now()

    def hours(self):
        return round((self.exit_time - self.entry_time).total_seconds() / 3600, 2)


# -----------------------------
# FINANCE CLASSES
# -----------------------------
class Transaction:
    def __init__(self, amount, ttype):
        self.amount = amount
        self.type = ttype
        self.date = datetime.now()


class Person:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        self.date = datetime.now()


class Debtor(Person):
    pass


class Creditor(Person):
    pass


class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.debtors = {}
        self.creditors = {}

    def add_revenue(self, amount):
        self.transactions.append(Transaction(amount, "revenue"))

    def add_expense(self, amount):
        self.transactions.append(Transaction(amount, "expense"))

    def total_revenue(self):
        return sum(t.amount for t in self.transactions if t.type == "revenue")

    def total_expense(self):
        return sum(t.amount for t in self.transactions if t.type == "expense")

    def profit(self):
        return self.total_revenue() - self.total_expense()

    def add_debtor(self, name, amount):
        self.debtors[name] = Debtor(name, amount)

    def add_creditor(self, name, amount):
        self.creditors[name] = Creditor(name, amount)

    def old_debtors(self):
        result = []
        for d in self.debtors.values():
            if (datetime.now() - d.date).days >= 30:
                result.append(d.name)
        return result


# -----------------------------
# REPORTING
# -----------------------------
class ReportManager:
    def __init__(self):
        self.sales = []

    def record_sale(self, pass_type, amount):
        self.sales.append((pass_type, amount, datetime.now()))

    def monthly_sales(self):
        total = 0
        for s in self.sales:
            total += s[1]
        return total

    def sales_by_type(self):
        result = {}
        for s in self.sales:
            result[s[0]] = result.get(s[0], 0) + s[1]
        return result


# -----------------------------
# PARKING SYSTEM
# -----------------------------
class ParkingSystem:
    def __init__(self):
        self.tickets = {}
        self.finance = FinanceManager()
        self.reports = ReportManager()

    def enter(self, plate, vtype):
        self.tickets[plate] = Ticket(Vehicle(plate, vtype))
        print("Vehicle entered")

    def exit(self, plate):
        ticket = self.tickets[plate]
        ticket.close_ticket()
        hours = ticket.hours()
        fee = hours * 5

        self.finance.add_revenue(fee)
        print(f"Fee: ${fee}")
        del self.tickets[plate]

    def buy_pass(self, plate, ptype):
        price = 100 if ptype == "monthly" else 30
        self.finance.add_revenue(price)
        self.reports.record_sale(ptype, price)
        print(f"{ptype} pass purchased")


# -----------------------------
# MAIN MENU
# -----------------------------
sys = ParkingSystem()

while True:
    print("\n1 Enter Vehicle")
    print("2 Exit Vehicle")
    print("3 Buy Monthly Pass")
    print("4 Buy Weekly Pass")
    print("5 Finance Summary")
    print("6 Reports")
    print("7 Exit")

    ch = input("Choice: ")

    if ch == "1":
        p = input("Plate: ")
        t = input("Type: ")
        sys.enter(p, t)

    elif ch == "2":
        p = input("Plate: ")
        sys.exit(p)

    elif ch == "3":
        sys.buy_pass("X", "monthly")

    elif ch == "4":
        sys.buy_pass("X", "weekly")

    elif ch == "5":
        print("Revenue:", sys.finance.total_revenue())
        print("Expense:", sys.finance.total_expense())
        print("Profit:", sys.finance.profit())

    elif ch == "6":
        print("Monthly Sales:", sys.reports.monthly_sales())
        print("Sales by Type:", sys.reports.sales_by_type())

    elif ch == "7":
        break
