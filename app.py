#import all the required modules
from model import (Base, session, Product, engine)
import csv
import datetime
from sys import exit
import time

#def a menu function to come back to in between tasks to ask the user where they would like to go
def menu():
    while True:
        print('''Please select an option:
                    v.) View a single products inventory
                    a.) Add a new product to the database
                    b.) Create a backup of the entire database
                    e.) Exit the program''')
        choice = input(">")
        if choice in ["v","a","b","e"]:
            return choice
        else:
            print("Please try again, remember to choose from v, a, or b")
#def cleaning functions to clean my data before it is put in a database and to clean the data the user puts in when making a product
def clean_price(price_string):
    try:
        return_price = int(float(price_string.lstrip('$')) * 100)
    except ValueError:
        input('''please input your price in the format $##.##
              press enter to continue > ''')
        return
    return return_price
def clean_quantity(quantity_string):
    try:
        quantity = int(quantity_string)
    except ValueError:
        input('''please enter a valid value
              this should be a number
              press enter to continue > ''')
        return
    return quantity
    
def clean_date(date_string):
    split_date = date_string.split("/")
    month = int(split_date[0])
    day = int(split_date[1].split(",")[0])
    year = int(split_date[2])
    return_date = datetime.date(month = month, day = day, year = year)
    return return_date
def clean_id(id, id_opt):
    try:
        id = int(id)
    except ValueError:
        input('''please input a valid id number
              you should enter a number
              press enter to continue > ''')
        return
    if id in id_opt:
        return id
    else:
        input('''please input a valid id number
              this should be within the range given
              press enter to continue > ''')
        return
#generate our csv and out backup csv file  
def add_csv():
    with open("inventory.csv") as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                name = row[0]
                price = clean_price(row[1])
                quantity = clean_quantity(row[2])
                date = clean_date(row[3])
                new_inventory = Product(product_name = name, product_price = price, product_quantity = quantity, date_updated = date)
                session.add(new_inventory)
        session.commit()
def generate_backup():

    with open("backup.csv", "w", newline='') as csvfile:
        productwriter = csv.writer(csvfile)

        productwriter.writerow(['product_id',
                                'product_name', 
                                'product_price', 
                                'product_quantity', 
                                'date_updated'])
        
        for product in session.query(Product).order_by(Product.product_id):
            productwriter.writerow([product.product_id,
                             product.product_name,
                             product.product_price,
                             product.product_quantity,
                             product.date_updated])
    print("The data has been backed-up")
#define our main app loop
def app():
    #create the loop and call on the necessary functions like the menu
    app_running = True
    while app_running:
        choice = menu()
        #compare the choice they chose to do the task requested
        if choice == "a" or choice == "A":
            #ask for the user input to create a new product
            name = input("name of your product: ")
            price_error = True
            while price_error:
                price = input("price of your product (Ex: $**.**): ")
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            quantity_error = True
            while quantity_error:
                quantity = input("quantity of your product: ")
                quantity = clean_quantity(quantity)
                if type(quantity) == int:
                    quantity_error = False
            date = datetime.datetime.today()
            new_product = Product(product_name = name, product_price = price, product_quantity = quantity, date_updated = date)
            session.add(new_product)
            session.commit()
            print("Product added!")
            time.sleep(1.5)
        elif choice == "v":
            #give the user options on the id to select and read the data of the product to the user
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            id_error = True
            while id_error:
                id_choice = input(f'''ID options: {id_options}
                book ID > ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Product).filter(product.product_id==id_choice).first()
            print(f'''
                  product name: {product.product_name}
                  product price: ${product.product_price / 100}
                  product quantity: {product.product_quantity}
                  last date updated: {product.date_updated}''')
            input("press enter when you would like to return to the main menu > ")
        elif choice == "b":
            #create a backup for the data so if it is lost it can be recovered
            generate_backup()
            input("press enter to continue to home page")
            time.sleep(1.5)
        elif choice == "e":
            #breaks the loop of the app if they choose to exit the code
            break
#creates a dunder main to call the functions and start the app
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()
    print("Goodbye!")