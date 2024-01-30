# Student ID: 010959749

# import utils
import sys
import datetime
import csv
import math

# import classes
import truck
import hash
import package

# initiate hash table
packageStorage = hash.HashTable()

# open and parse csv files
with open("files/address_file.csv") as address:
    AddressContent = csv.reader(address)
    AddressContent = list(AddressContent)

with open("files/distance_file.csv") as distance:
    DistanceContent = csv.reader(distance)
    DistanceContent = list(DistanceContent)


# function to parse and load packages into hash table
def load_packages():
    # open and parse package file
    with open("files/package_file.csv") as packages:
        package_content = csv.reader(packages, delimiter=",")

        # iterate over fields, create a package object, insert package into hash table
        for data in package_content:
            package_data = package.Package(int(data[0]), data[1], data[2], data[3], data[4], data[5], data[6])
            packageStorage.insert(int(data[0]), package_data)


# function to find address id given an address name
# returns the id from the parsed address content
def find_address_id(addressName):
    for row in AddressContent:
        if addressName in row[2]:
            return int(row[0])


# function to distance from an address to the other
# searches parsed distance table for values
# returns the distance as a float number
def find_distance_between(address, addressToCompare):
    distance = DistanceContent[address][addressToCompare]
    if distance == "":
        distance = DistanceContent[addressToCompare][address]
    return float(distance)


# call package loading procedure
load_packages()

# load trucks and add packages
truck1 = truck.Truck(0.0, "4001 South 700 East", datetime.timedelta(hours=8),[15, 1, 13, 16, 19, 14, 20, 27, 34, 37, 40, 29, 30, 31])
truck2 = truck.Truck(0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20),[2, 3, 4, 18, 36, 38, 5, 9, 26, 28, 32, 35])
truck3 = truck.Truck(0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),[6, 7, 8, 12, 10, 11, 17, 21, 22, 23, 39, 24, 25, 33])


# function to load and deliver packages depending on their address
# time complexity O(n^2)
def load_and_deliver(truck):
    # initiate packages at the hub
    packagesAtHub = []

    # load packages to hub
    for packageID in truck.packages:
        packagesAtHub.append(packageStorage.search(packageID))

    # empty initial packages in truck
    truck.packages.clear()
    truck.current_time = truck.depart_time

    # run until no more packages left
    while len(packagesAtHub) > 0:
        # initiate distance and next package
        nextDistance = math.inf
        nextPackage = None

        # iterate over packages at hub
        for package in packagesAtHub:
            # find and set distance between truck and package
            distance = find_distance_between(find_address_id(truck.address), find_address_id(package.address))
            # if distance is the smallest yet, set the next distance and package
            if distance <= nextDistance:
                nextDistance = distance
                nextPackage = package

        # remove package from the hub
        packagesAtHub.remove(nextPackage)

        # add packages to truck, set truck address, and increment miles and time
        truck.packages.append(nextPackage.id)
        truck.miles += nextDistance
        truck.address = nextPackage.address
        truck.current_time += datetime.timedelta(hours=nextDistance / 18)

        # update departure and delivery times
        nextPackage.departure_time = truck.depart_time
        nextPackage.delivery_time = truck.current_time


# load and send truck 1 and 3 on delivery
load_and_deliver(truck1)
load_and_deliver(truck3)

# wait till on of the trucks return, send truck 2 on delivery
truck2.depart_time = min(truck1.current_time, truck3.current_time)
load_and_deliver(truck2)


# function to print package status from entered time and package id
# return error if not found
def print_package_status(entered_time, package_id):
    package_item = packageStorage.search(package_id)
    if package_item is None:
        print("Package was not found")
        return

    package_item.setStatus(entered_time)
    print(package_item.printStatus())


# prints UI header
def start_ui():
    print(" --------------------------------------")
    print("|  Welcome to WGUPS Routing Program    |")
    print(" --------------------------------------\n")
    print("Total Miles: ", truck1.miles + truck2.miles + truck3.miles, " miles")
    print("Please input one of the following options")
    print("| (1) to Quit | (2) to Search Package Status | (3) to View All Packages Report |")


# initiates UI header
start_ui()
# print("Truck 1: ", truck1.miles, " miles")
# print("Truck 2: ", truck2.miles, " miles")
# print("Truck 3: ", round(truck3.miles, 2), " miles")

while True:
    keyboard_input = input("Input: ")

    # proceed depending on user input
    match keyboard_input:
        case "1":
            # stop running
            sys.exit()
        case "2":
            # allow user to input time and package id
            # call package status procedure
            print("--- Package Status Tracking ---")
            try:
                time_input = input("Please enter time in HH:MM format: ")
                (hour, minutes) = time_input.split(":")
                time = datetime.timedelta(hours=int(hour), minutes=int(minutes))

                package_input = input("Please enter a package ID: ")
                id = int(package_input)
                print_package_status(time, id)
            except ValueError:
                print("Unknown package ID or format")
                pass
        case "3":
            # allow user to input time
            # call package status procedure for all packages
            print("--- All Packages Status Report ---")
            try:
                time_input = input("Please enter time in HH:MM format: ")
                (hour, minutes) = time_input.split(":")
                time = datetime.timedelta(hours=int(hour), minutes=int(minutes))

                for packageID in range(1, (len(packageStorage.table) + 1)):
                    print_package_status(time, packageID)
            except ValueError:
                print("Unknown format")
                pass
        case _:
            print("Sorry that command is not recognized")
