from model import (Base, session, inventory, engine)
import csv
import datetime
from sys import exit
import time


def menu():
    while True:
        print('''Please select an option:
                    v.) View a single products inventory
                    a.) Add a new product to the database
                    b.) Create a backup of the entire database''')
        choice = input(">")
        if choice in ["v", "a", "b", "V", "A", "B"]:
            return choice
        else:
            print("Please try again, remember to choose from v, a, or b")
def clean_price(price_string):
    return int(float(price_string.lstrip('$')) * 100)
def clean_quantity(quantity_string):
    return int(quantity_string)
def clean_date(date_string):
    split_date = date_string.split("/")
    month = int(split_date[0])
    day = int(split_date[1].split(",")[0])
    year = int(split_date[2])
    return datetime.date(year = year, month = month, day = day)
def add_csv():
    with open("inventory.csv") as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_in_db = session.query(inventory).filter(inventory.product_name==row[0]).one_or_none()
            if product_in_db == None:
                name = row[0]
                price = clean_price(row[1])
                quantity = clean_quantity(row[2])
                date = clean_date(row[3])
                new_inventory = inventory(product_name = name, product_price = price, product_quantity = quantity, date_updated = date)
                session.add(new_inventory)
        session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    add_csv()
    
    for product in session.query(inventory):
        print(product)