from abc import ABC, abstractmethod
from datetime import datetime

# ABSTRACT PRICING STRATEGY

class PricingStrategy(ABC):

    @abstractmethod
    def calculate_fee(self, hours, vehicle_type):
        pass


class PeakPricing(PricingStrategy):
    def calculate_fee(self, hours, vehicle_type):
        rate = 5
        if vehicle_type == "bike":
            rate = 2
        return hours * rate


class OffPeakPricing(PricingStrategy):
    def calculate_fee(self, hours, vehicle_type):
        rate = 3
        if vehicle_type == "bike":
            rate = 1
        return hours * rate



# VEHICLE CLASS
# -------------------------
class Vehicle:
    def __init__(self, plate, vtype):
        self.plate = plate
        self.vtype = vtype


# -------------------------
# PASS (ABSTRACT)
# -------------------------
class Pass(ABC):
    def __init__(self, plate):
        self.plate = plate

    @abstractmethod
    def is_valid(self):
        pass


class MonthlyPass(Pass):
    def __init__(self, plate):
        super().__init__(plate)
        self.start_date = datetime.now()

    def is_valid(self):
        return True


class WeeklyPass(Pass):
    def __init__(self, plate):
        super().__init__(plate)
        self.start_date = datetime.now()

    def is_valid(self):
        return True


# -------------------------
# TICKET CLASS
# -------------------------
class Ticket:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.entry_time = datetime.now()
        self.exit_time = None

    def close_ticket(self):
        self.exit_time = datetime.now()

    def get_hours(self):
        diff = self.exit_time - self.entry_time
        return round(diff.total_seconds() / 3600, 2)


# -------------------------
# PARKING SPACE
# -------------------------
class ParkingSpace:
    def __init__(self, number):
        self.number = number
        self.is_free = True


# -------------------------
# PARKING LOT
# -------------------------
class ParkingLot:
    def __init__(self, capacity):
        self.spaces = [ParkingSpace(i) for i in range(1, capacity+1)]
        self.tickets = {}
        self.passes = {}
        self.pricing = PeakPricing()

    def add_pass(self, pass_obj):
        self.passes[pass_obj.plate] = pass_obj

    def find_free_space(self):
        for s in self.spaces:
            if s.is_free:
                return s
        return None

    def enter_vehicle(self, plate, vtype):
        space = self.find_free_space()
        if space is None:
            print("Parking Full")
            return

        vehicle = Vehicle(plate, vtype)
        ticket = Ticket(vehicle)
        self.tickets[plate] = ticket
        space.is_free = False

        print(f"Vehicle parked at space {space.number}")

    def exit_vehicle(self, plate):
        if plate not in self.tickets:
            print("Vehicle not found")
            return

        ticket = self.tickets[plate]
        ticket.close_ticket()
        hours = ticket.get_hours()

        if plate in self.passes and self.passes[plate].is_valid():
            fee = 0
        else:
            fee = self.pricing.calculate_fee(hours, ticket.vehicle.vtype)

        del self.tickets[plate]

        for s in self.spaces:
            if not s.is_free:
                s.is_free = True
                break

        print(f"Hours Parked: {hours}")
        print(f"Fee: ${fee}")

    def available_spaces(self):
        free = sum(1 for s in self.spaces if s.is_free)
        print(f"Available spaces: {free}")


# -------------------------
# MAIN PROGRAM
# -------------------------
lot = ParkingLot(300)

while True:
    print("\n--- Parking System ---")
    print("1. Enter Vehicle")
    print("2. Exit Vehicle")
    print("3. Add Monthly Pass")
    print("4. Add Weekly Pass")
    print("5. Show Available Spaces")
    print("6. Exit Program")

    choice = input("Choose: ")

    if choice == "1":
        plate = input("Plate: ")
        vtype = input("Type (car/bike): ")
        lot.enter_vehicle(plate, vtype)

    elif choice == "2":
        plate = input("Plate: ")
        lot.exit_vehicle(plate)

    elif choice == "3":
        plate = input("Plate: ")
        lot.add_pass(MonthlyPass(plate))
        print("Monthly pass added")

    elif choice == "4":
        plate = input("Plate: ")
        lot.add_pass(WeeklyPass(plate))
        print("Weekly pass added")

    elif choice == "5":
        lot.available_spaces()

    elif choice == "6":
        break

    else:
        print("Invalid choice")
