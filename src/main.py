import sys
import os
import locale
import urllib.request
import urllib.parse

from datamodule import RowNotFound, Data
from pymitter import EventEmitter

ee = EventEmitter()
locale.setlocale( locale.LC_ALL, '' )
key = "&key=" + ""

command_dict = {
    "list": "Lists all commands",
    "find": "Searches for house",
    "average": "Displays the average house price",
    "most expensive": "Displays the most expensive house price",
    "least expensive": "Displays the least expensive house price",
    "custom search": "Searches for houses based on a query of your choice",
    "picture": "Saves a picture of this house using the google maps streetview API",
    "exit": "Exists the program",
    "clear": "Clears the screen"
}

command_tuple = (
    'list', 
    'find', 
    'average', 
    'most expensive', 
    'least expensive', 
    'custom search',
    "picture",
    "exit",
    "clear"
)

param_tuple = (
    "longitude", 
    "latitude", 
    "price", 
    "sale_date", 
    "type", 
    "sq__ft", 
    "baths", 
    "beds", 
    "state", 
    "zip", 
    "city", 
    "street"
)

type_dict = {
    "longitude": "int",
    "latitude": "int",
    "price": "int",
    "sale_date": "str",
    "type": "str",
    "sq__ft": "int",
    "baths": "int",
    "beds": "int",
    "state": "str",
    "zip": "str",
    "city": "str",
    "street": "str"
}

def getStreet(address, pic_location='./pictures'):
  base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
  MyUrl = base + urllib.parse.quote_plus(address) + key #added url encoding
  fi = address + ".jpg"
  urllib.request.urlretrieve(MyUrl, os.path.join(pic_location,fi))

@ee.on("list")
def listCmds():
    for cmd in command_dict:
        print("Command {} = {}\n".format(cmd, command_dict[cmd]))
    main()

@ee.on("find")
def findHouse():
    house = input("Please enter the house you want to search for! (format = street,city) ")
    try:
        row = Data.findRow(house)
        module = Data(row)

        print("Street: {}\nCity: {}\nZip: {}\nState: {}\n#Beds: {}\n#Baths: {}\nSquare Feet: {}\nType: {}\nSale Date: {}\nPrice: {}\nLatitude: {}\nLongitude: {}".format(
            module.getStreet(),
            module.getCity(),
            module.getZip(),
            module.getState(),
            module.getBeds(),
            module.getBaths(),
            module.getSqrFT(),
            module.getType(),
            module.getSaleDate(),
            locale.currency(int(module.getPrice()), grouping=True),
            module.getLatitude(),
            module.getLongitude()
        ))
        main()

    except RowNotFound:
        print("Could not find house...")
        main()

@ee.on("average")
def getAverage():
    average = Data.getAveragePrice()
    print("The average price out of all the houses is {}.".format(
        locale.currency(average, grouping=True)
    ))
    main()

@ee.on("mostexpensive")
def mostExpensive():
    most = Data.getMostExpensive()
    price = most.price

    print("The most expensive house out of all the houses is {}".format(locale.currency(price, grouping=True)))
    main()

@ee.on("leastexpensive")
def leastExpensive():
    least = Data.getLeastExpensive()
    price = least.price

    print("The least expensive house out of all the houses is {}".format(locale.currency(price, grouping=True)))
    main()

@ee.on("customsearch")
def customSearch():
    search_type = input("What variable do you want to search for? ")
    if not validParam(search_type):
        print("Invalid variable name. Please try again! ")
        main()
    
    value = input("What do you want the value of this variable to be? ")
    if type_dict[search_type] == "str":
        value = str(value)
    elif type_dict[search_type] == "int":
        value = int(value)
    
    query = Data.Query(search_type=search_type, value=value)
    for p in query:
        print("Street: {}\nCity: {}\nZip: {}\nState: {}\n#Beds: {}\n#Baths: {}\nSquare Feet: {}\nType: {}\nSale Date: {}\nPrice: {}\nLatitude: {}\nLongitude: {}\n\n".format(
            p.street,
            p.city,
            p.zip,
            p.state,
            p.beds,
            p.baths,
            p.sq__ft,
            p.type,
            p.sale_date,
            locale.currency(p.price, grouping=True),
            p.latitude,
            p.longitude
        ))
    main()

@ee.on("picture")
def picture():
    address = input("What is the address of this house. (format = street, city, state zip) ")
    getStreet(address)
    main()

@ee.on("exit")
def _exit():
    print("Goodbye...")
    sys.exit()

@ee.on("clear")
def clear():
    os.system("cls")
    main()

def validCommand(cmd):
    return cmd.lower() in command_tuple

def validParam(param):
    return param in param_tuple

def banner():
    banner = "-" * 10 + '\n' + "DATA MINER" + "\n" + "-" * 10
    print(banner)

def main():
    directory = "./pictures"
    if not os.path.exists(directory):
        print("Making pictures directory for google image pictures...")
        os.makedirs(directory)
    
    cmd = input("Please enter a command. (type 'list' for a list of commands) ")
    if not validCommand(cmd):
        print("Invalid Command. Try again...")
        main()
    cmd = cmd.lower().replace(" ", "")
    ee.emit(cmd)

if __name__ == "__main__":
    banner()
    main()