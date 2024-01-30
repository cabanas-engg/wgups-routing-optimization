import datetime

# package class to model packages
class Package:
    departure_time = None
    delivery_time = None
    status = "At the Hub"

    def __init__(self, id, address, city, state, zipcode, deadline, weight):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight

    def __str__(self):
        return f'({self.id}, {self.address}, {self.city}, {self.state}, {self.zipcode},{self.deadline},{self.weight},{self.departure_time},{self.delivery_time},{self.status})'

    # prints status of package object by displaying some attributes
    def printStatus(self):
        return f'(ID: {self.id}, Address: {self.address}, Status: {self.status}, Deadline: {self.deadline}, Departure: {self.departure_time}, Delivery: {self.delivery_time})'

    # checks and sets status of package depending on passed time in HH:MM format
    def setStatus(self, time_check):
        if self.delivery_time == None or time_check < self.departure_time:
            self.status = "At the Hub"
        elif time_check < self.delivery_time:
            self.status = "En Route"
        else:
            self.status = "Delivered"

        # change package address for package with wrong address
        if self.id == 9 and (time_check > datetime.timedelta(hours=10, minutes=20)):
            self.address = "410 S State St"
            self.zipcode = "84111"
