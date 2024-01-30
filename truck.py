# truck class to model trucks
class Truck:
    capacity = 16
    speed = 18

    def __init__(self, miles, address, depart_time, packages):
        self.miles = miles
        self.address = address
        self.depart_time = depart_time
        self.packages = packages
        self.current_time = depart_time

    def __str__(self):
        return f'({self.capacity},{self.speed},{self.packages},{self.miles},{self.address},{self.depart_time})'
