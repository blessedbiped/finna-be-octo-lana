# original code from https://levelup.gitconnected.com/building-a-simple-inventory-inventory-system-with-python-and-sqlite-4382fbd6c596
# modified for my boxes for inventory system
import sqlite3
import time
#import fts5

class Product():
    def __init__(self, name, box):
        self.name = name
        self.box = box
        
    def __str__(self):
        return "Item Name: {}\nBox: ".format(self.name, self.box)


class inventory():
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = sqlite3.connect('inventory.db')
        self.cursor = self.conn.cursor()
        query = "Create Table if not exists inventory(name TEXT, box TEXT)"
        self.cursor.execute(query)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def add_product(self, product):
        query = "INSERT INTO inventory values(?, ?)"
        self.cursor.execute(query,(product.name, product.box))
        self.conn.commit()
    
    def remove_product(self,name):
        query = "DELETE FROM inventory WHERE name =?"
        self.cursor.execute(query,(name,))
        self.conn.commit() 
    
    def list_products(self):
        query = "SELECT * FROM inventory"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if rows: 
            for row in rows:
                print("Item Name: {}\tBox: {} \n".format(row[0],row[1]))
        else:
            print("No match")
    
    def update_product(self, product):
        query = "UPDATE inventory SET box =?, WHERE name =?"
        self.cursor.execute(query, (product.box, product.name))
        self.conn.commit() 

    def search_product(self, name):
        # create FTS5 table and index
        #self.conn.execute('CREATE VIRTUAL TABLE IF NOT EXISTS products USING fts5(name, box)')
        name = '%' + name + '%'
        # perform search
        results = self.conn.execute('SELECT * FROM inventory WHERE name LIKE (?)', (name,))
        rows = results.fetchall()
        if rows:
            for row in rows:
                print("Item Name: {}\t\tBox: {}\n".format(row[0], row[1]))
        else:
            print("Product not found")

    def list_boxes(self,boxname):
        query = self.conn.execute("SELECT * FROM inventory WHERE box LIKE (?)",(boxname,))
        rows = query.fetchall()
        if rows:
            for row in rows:
                print("Item Name: {}\t\tBox: {} \n".format(row[0],row[1]))
        else:
            print("No box with that name found\n") 

    print(""" 
          1.Add product 
          2.Remove product
          3.List All Products
          4.Update Product #not available
          5.Search Product
          6.Exit

          """)
# TODO: list by box
    
inventory = inventory()

while True:
    choice = input("Enter your choice: ")
    
    if int(choice) == 1:
        name = input("Enter name: ")
        box = input("Enter box: ")
        new_product = Product(name, box)

        print("{} is being added".format(name))
        time.sleep(0.2)
        inventory.add_product(new_product)
        print("{} added".format(name))

    elif int(choice) == 2:
        name = input("Enter item name: ")

        print("{} is being removed\n".format(name))
        time.sleep(0.2)
        inventory.remove_product(name)
        print("{} removed\n".format(name))

    elif int(choice) == 3:
        inventory.list_products()
        #print("Listing products")
        #print("Products are listed")

    elif int(choice) == 4: # need to search first and return, then update. no blind updating!
        name = input("Enter name to update: ")
        price = input("Enter box to update: ")
        new_product = Product(name, box)

        print("Updating {}\n".format(name))
        time.sleep(0.2)
        inventory.update_product(new_product)
        print("{} has been updated\n".format(name))

    elif int(choice) == 5:
        name = input("Enter item to search: ") 
        print("Looking for {} in the database\n".format(name))
        time.sleep(0.2)
        inventory.search_product(name)
        
    elif int(choice) == 6:
        break

    else:
        print("Invalid choice, try again\n")