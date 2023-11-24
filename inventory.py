# importing the functions i need like the os function to locate files 
# and the tabulate to use the grip function to organize my data
import os
from tabulate import tabulate

# locating txt files for the rest of the code to use with ease
script_directory = os.path.dirname(os.path.abspath(__file__ if "__file__" in locals() else __file__))
file_path = os.path.join(script_directory, 'inventory.txt')

# class to define all the shoe attributes
class Shoe:
    # class instance attributes
    def __init__(self, code, product,country, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
    # class string representation
    def __str__(self):
        return f"Shoe Code: {self.code}\nProduct: {self.product}\nPrice: ${self.cost:.2f}\nQuantity: {self.quantity}"

# function  to go through the txt file and 
# then print all the data in a nice grid for ease of viewing
def read_shoe_data(file_path):
    shoes_list = []
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) > 1:
                header = lines[0].strip()
                if header == "Country,Code,Product,Cost,Quantity":
                    for line in lines[1:]:
                        elements = line.strip().split(',')
                        if len(elements) == 5:  
                            country, code, product, cost, quantity = elements
                            price = float(cost)
                            quantity = int(quantity)
                            shoe = Shoe(code, product, country, price, quantity)
                            shoes_list.append(shoe)
            else:
                print("File is empty or does not contain shoe data.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return shoes_list

# load shoe data from the txt inventory file
shoes_list = read_shoe_data(file_path)

# function to find a shoe ion the txt file based on the given code
# the program will go through the txt file and find if the code matches any code 
# in the file and if so will print that colum in the list of shoes
# if not then error message will be displayed
def capture_shoe(shoes_list):
    print("Capture Shoe Data:")
    code = input("Enter the shoe code: ")
    product = input("Enter the product name: ")
    country = input("Enter the country: ")  

    try:
        cost = float(input("Enter the shoe price: $"))
        quantity = int(input("Enter the shoe quantity: "))

        shoe = Shoe(code, product, country, cost, quantity)  
        shoes_list.append(shoe)
        print("Shoe data captured and added to the list.")

        save_shoe_data(shoes_list)
    except ValueError:
        print("Invalid input. Please enter a valid price and quantity.")

# function to take new shoe data and then add it to the txt inventory file
# the added shoe with all appropriate data will be saved for future use
def save_shoe_data(shoes_list):
    with open(file_path, "w") as file:
        file.write("Country,Code,Product,Cost,Quantity\n")
        for shoe in shoes_list:
            file.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n")

# function to display all of the shoes in the txt inventory file
def display_shoes(shoes_list):
    if not shoes_list:
        print("No shoes to display.")
    else:
        table_data = []
        for shoe in shoes_list:
            table_data.append([shoe.country, shoe.code, shoe.product, f"${shoe.cost:.2f}", shoe.quantity])

        headers = ["Country", "Shoe Code", "Product", "Price", "Quantity"]
        table = tabulate(table_data, headers, tablefmt="grid")
        print("Shoe Details:")
        print(table)

# this function is if the user wants to update the stock of shoes 
# the program will show the user the lowest shoe stocked and then 
# as the user if they want to add more stock
def re_stock(shoes_list):
    if not shoes_list:
        print("No shoes in the list.")
        return

    lowest_quantity_shoe = min(shoes_list, key=lambda shoe: shoe.quantity)

    print("Shoe with the lowest quantity:")
    print(f"Country: {lowest_quantity_shoe.country}")
    print(f"Product: {lowest_quantity_shoe.product}")
    print(f"Price: ${lowest_quantity_shoe.cost:.2f}")
    print(f"Quantity: {lowest_quantity_shoe.quantity}")

    restock_input = input("Do you want to restock this item? (yes/no): ").strip().lower()

    if restock_input == "yes":
        try:
            additional_quantity = int(input("Enter the quantity to restock: "))
            lowest_quantity_shoe.quantity += additional_quantity
            print("Restocked successfully.")

            save_shoe_data(shoes_list)
        except ValueError:
            print("Invalid quantity input. Restock failed.")

# this function is if the user wants to locate a specific shoe based on a code
# the program will go through the file making sure to skip the heading and see 
# if said shoe is in the file if that is the case it will print that shoes data
def find_shoe_by_code(file_path, target_code):
    try:
        with open(file_path, 'r') as file:
            next(file)  # Skip the header
            found = False
            for line in file:
                elements = line.strip().split(',')
                if len(elements) >= 4:
                    country, code, product, cost, quantity = elements[:5]  # Use the first 5 elements
                else:
                    continue  # Skip invalid lines

                if code == target_code:
                    print(f"Found code '{target_code}' in the file.")
                    print(f"Country: {country}")
                    print(f"Product: {product}")
                    print(f"Price: ${float(cost):.2f}")
                    print(f"Quantity: {int(quantity)}")
                    found = True
                    break
            if not found:
                print(f"Code '{target_code}' not found in the file.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# this function is for if the user wants to 
def calculate_and_display_total_value(shoes_list):
    total_values = {}

    for shoe in shoes_list:
        try:
            total_price = shoe.cost * shoe.quantity
            if (shoe.country, shoe.product) in total_values:
                total_values[(shoe.country, shoe.product)] += total_price
            else:
                total_values[(shoe.country, shoe.product)] = total_price
        except ValueError:
            print(f"Invalid cost for shoe with code '{shoe.code}'.")

    if not total_values:
        print("No shoes to display.")
    else:
        table_data = []
        for (country, product), total_value in total_values.items():
            table_data.append([country, product, f"${total_value:.2f}"])

        headers = ["Country", "Product", "Total Value"]
        table = tabulate(table_data, headers, tablefmt="grid")
        print("Total Value per Item:")
        print(table)


# this function is to be used by the user if they 
# want to see the shoe with the highest quantity
def highest_qty(shoes_list):
    if not shoes_list:
        print("No shoes in the list.")
        return

    highest_quantity_shoe = max(shoes_list, key=lambda shoe: shoe.quantity)

    print("Shoe with the highest quantity:")
    print(f"Country: {highest_quantity_shoe.country}")
    print(f"Product: {highest_quantity_shoe.product}")
    print(f"Price: ${highest_quantity_shoe.cost:.2f}")
    print(f"Quantity: {highest_quantity_shoe.quantity}")


# this is the menu loop where the user will
# be shown a menu where they can 
# select options to call specified functions to 
# do certain tasks
while True:
    # menu
    print('''
    Pick which option you want to use:
    1 ----> [See Shoe Data]
    2 ----> [Add A Shoe]
    3 ----> [View All Shoes]
    4 ----> [Update Shoe Stocks]
    5 ----> [Search For A Shoe]
    6 ----> [See Shoe total stock Values]
    7 ----> [See Shoe Highest Stocked Shoe]
    8 ----> [Exit]
    ''')
    user_choice = input("Enter Your Choice Here: ")

# logic for users choice from the menu
    if user_choice == "1":
        display_shoes(shoes_list)
    elif user_choice == "2":
        capture_shoe(shoes_list)
    elif user_choice == "3":
        display_shoes(shoes_list)
    elif user_choice == "4":
        re_stock(shoes_list)
    elif user_choice == "5":
        user_target_code = input("Enter the code you want to search for: ")
        find_shoe_by_code(file_path, user_target_code)
    elif user_choice == "6":
        calculate_and_display_total_value(shoes_list)
    elif user_choice == "7":
        highest_qty(shoes_list)
    elif user_choice == "8":
        print("Cheers!")
        break
    else:
        print("Invalid input, please try again!")