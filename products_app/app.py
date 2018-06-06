import csv
import os

def menu(username="username", products_count="100"):
    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Welcome {username}!
    There are {products_count} products in the database.
        operation | description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product.
        'Reset'   | Reset to the original csv file."""
    return menu

def read_products_from_file(filename="products.csv"):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    products = []
    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            products.append(dict(row))
    return products

def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "name", "aisle", "department", "price"])
        writer.writeheader() # uses fieldnames set above
        for a in products:
            writer.writerow(a)

def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print("RESETTING DEFAULTS")
    products = read_products_from_file(from_filename)
    write_products_to_file(filename, products)

def auto_id(products):
    all_ids = [int(p_id["id"]) for p_id in products]
    max_id = max(all_ids)
    auto_id = max_id + 1
    return auto_id

def matching_product(x):
    products = read_products_from_file()
    position = 0
    for p in products:
        if p["id"] == x:
            return position
        position += 1

def run():
    products = read_products_from_file()
    print(menu(username=str(input("Please enter your username: ")),products_count=len(products)))
    while True:
        operation_selected = input("Please select an operation, or 'DONE' if there is no operation required: ")
        operation_selected = operation_selected.title()

        if operation_selected == "Done":
            break

        if operation_selected == "List":
            print("-----------------------------------")
            print("LISTING " + str(len(products)) + " PRODUCTS")
            print("-----------------------------------")
            for single_product in products:
                print("#" + single_product["id"] + ": " + single_product["name"])

        if operation_selected == "Show":
            position = matching_product(input("Please input a product identifier: "))
            print(f"""
-----------------------------------
SHOWING A PRODUCT
-----------------------------------""")
            print(products[position]
            )

        if operation_selected == "Create":
            id = auto_id(products)
            name = input("Please enter product name: ")
            valid_aisle = ["1", "2", "3", "4", "5"]
            aisle = str(input("Please enter product aisle (1, 2, 3, 4, 5): "))
            while True:
                if aisle not in valid_aisle:
                    print("Error: only these aisles can be selected (1, 2, 3, 4, 5)")
                    aisle = str(input("Please enter product aisle from (1, 2, 3, 4, 5): "))
                else:
                    break
            valid_department = ["1", "2", "3", "4", "5"]
            department = str(input("Please enter product deparment from (1, 2, 3, 4, 5): "))
            while True:
                if department not in valid_department:
                    print("Error: only these departments can be selected (1, 2, 3, 4, 5)")
                    department = str(input("Please enter product department from (1, 2, 3, 4, 5): "))
                else:
                    break
            try:
                price=float(input("Please enter product price: "))
            except ValueError:
                print("Error: Please use a number for price, like 0.77")
                price=float(input("Please enter product price: "))
            new_product = {"id": str(id), "name": str(name), "aisle": str(aisle), "department": str(department), "price": str(price)}
            products.append(new_product)
            write_products_to_file(products=products)
            print(f"""
-----------------------------------
CREATING A PRODUCT
-----------------------------------""")
            print(new_product)

        if operation_selected == "Update":
            position = matching_product(input("Please input a product identifier: "))
            print(products[position])
            products[position]["id"] = input("Please enter new product id: ")
            products[position]["name"] = input("Please enter new product name: ")
            valid_aisle = ["1", "2", "3", "4", "5"]
            products[position]["aisle"] = str(input("Please enter product aisle (1, 2, 3, 4, 5): "))
            while True:
                if products[position]["aisle"] not in valid_aisle:
                    print("Error: only these aisles can be selected (1, 2, 3, 4, 5)")
                    products[position]["aisle"] = str(input("Please enter product aisle from (1, 2, 3, 4, 5): "))
                else:
                    break
            valid_department = ["1", "2", "3", "4", "5"]
            products[position]["department"] = str(input("Please enter product deparment from (1, 2, 3, 4, 5): "))
            while True:
                if products[position]["department"] not in valid_department:
                    print("Error: only these departments can be selected (1, 2, 3, 4, 5)")
                    products[position]["department"] = str(input("Please enter product department from (1, 2, 3, 4, 5): "))
                else:
                    break
            try:
                price=float(input("Please enter product price: "))
            except ValueError:
                print("Error: Please use a number for price, like 0.77")
                price=float(input("Please enter product price: "))
            products[position]["price"] = price

            print(f"""
-----------------------------------
UPDATING A PRODUCT
-----------------------------------""")
            print(products[position])
        if operation_selected == "Destroy":
            position_delete = matching_product(input("Please input a product identifier: "))
            print(f"""
-----------------------------------
DESTROYING A PRODUCT
-----------------------------------""")
            print(products[position_delete])
            products.remove(products[position_delete])
        if operation_selected == "Reset":
            reset_products_file()
            return products
        valid_operations = ["Destroy", "Create", "Update", "List", "Show", "Reset"]
        if operation_selected not in valid_operations:
            print("Unrecognized Operation. Please choose one of: 'List', 'Show', 'Create', 'Update', or 'Destroy'")

    # Finally, save products to file so they persist after script is done...
    write_products_to_file(products=products)

# only prompt the user for input if this script is run from the command-line
# this allows us to import and test this application's component functions
if __name__ == "__main__":
    run()
