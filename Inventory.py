# This project uses a graphical user interface therefore the tkinter library must be installed before running
# https://docs.python.org/3/library/tkinter.html
# https://www.geeksforgeeks.org/how-to-install-tkinter-on-macos/
# https://www.activestate.com/resources/quick-reads/how-to-install-tkinter-in-windows/

from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview


# ------------------------------------------------------------------------------------------------------------
# ========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_country(self):
        return self.country

    def get_code(self):
        return self.code

    def get_product(self):
        return self.product

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def price(self):
        p = float(self.cost) * float(self.quantity)
        return str(f"£ {p}")

    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}\n"

    def set_quantity(self, quantity):
        new = int(self.quantity) + int(quantity)
        self.quantity = new
        return self.quantity


# --------------------------------------Outside the class -----------------------------------------

shoe_list = []


# Reads inventory.txt and formats each line to be able to create a new Shoe() object and append to shoe_list
# If the file does not exist then the program will not continue

def read_shoes_data():
    try:
        with open("inventory.txt", "r") as r:
            for line in r:
                temp = line.strip("\n")
                temp = temp.split(",")
                shoe_list.append(Shoe(temp[0], temp[1], temp[2], temp[3], temp[4]))
            shoe_list.pop(0)

    except FileNotFoundError:
        print(f"File Does Not Exist, Please Create 'inventory.txt'")
        quit()


# Prints all data from shoe_list to the command line

def view_all():
    for shoe in shoe_list:
        print(shoe)


# Populates the table with data from shoe_list, also uses the method price() to display the price in the table

def fill_table():
    for shoe in shoe_list:
        table.insert("", "end",
                     values=(
                         shoe.get_country(), shoe.get_code(), shoe.get_product(), shoe.get_cost(), shoe.get_quantity(),
                         shoe.price()))


# Deletes all data from the table

def empty_table():
    for i in table.get_children():
        table.delete(i)


# Searches shoe_list to find and return the Shoe() object with the lowest quantity

def lowest_quantity():
    minimum = shoe_list[0]

    for shoe in shoe_list:
        if int(shoe.get_quantity()) < int(minimum.get_quantity()):
            minimum = shoe

    return minimum


# -------------------------TOP LEVEL WINDOWS-----------------------------------------------------------------------------

# Creates a top level window and widgets for adding another shoe to shoe_list
# Once the submit button is pressed this takes all the input from the entry fields and uses this to create a new object of Shoe()
# and append this to the shoe_list

def capture_shoe():
    top = Toplevel(window)
    top.title("Add Shoe")
    top.resizable(False, False)

    lbl_country = Label(top, text="Country:")
    lbl_code = Label(top, text="Code:")
    lbl_product = Label(top, text="Product:")
    lbl_cost = Label(top, text="Cost:")
    lbl_quantity = Label(top, text="Quantity:")

    entry_country = Entry(top)
    entry_code = Entry(top)
    entry_product = Entry(top)
    entry_cost = Entry(top)
    entry_quantity = Entry(top)

    lbl_country.grid(row=0, column=0, padx=5, pady=5, sticky=N + E + S + W, columnspan=2, ipadx=10)
    lbl_code.grid(row=1, column=0, padx=5, pady=5, sticky=N + E + S + W, columnspan=2)
    lbl_product.grid(row=2, column=0, padx=5, pady=5, sticky=N + E + S + W, columnspan=2)
    lbl_cost.grid(row=3, column=0, padx=5, pady=5, sticky=N + E + S + W, columnspan=2)
    lbl_quantity.grid(row=4, column=0, padx=5, pady=5, sticky=N + E + S + W, columnspan=2)

    entry_country.grid(row=0, column=2, padx=5, pady=5, sticky=N + E + S + W, columnspan=2, ipadx=20)
    entry_code.grid(row=1, column=2, padx=5, pady=5, sticky=N + E + S + W, columnspan=2)
    entry_product.grid(row=2, column=2, padx=5, pady=5, sticky=N + E + S + W, columnspan=2)
    entry_cost.grid(row=3, column=2, padx=5, pady=5, sticky=N + E + S + W, columnspan=2)
    entry_quantity.grid(row=4, column=2, padx=5, pady=5, sticky=N + E + S + W, columnspan=2)

    def submit_btn():

        try:
            shoe_list.append(
                Shoe(entry_country.get(), entry_code.get(), entry_product.get(), float(entry_cost.get()),
                     float(entry_quantity.get())))
            top.destroy()
            print("Shoe Added")

            empty_table()
            fill_table()

        except ValueError:

            print("Could Not be Added : Cost and Quantity must be numerical")
            entry_cost.delete(0, END)
            entry_quantity.delete(0, END)

    btn_add_submit = Button(top, text="Submit", borderwidth=2, command=submit_btn)
    btn_add_submit.grid(row=5, column=0, columnspan=4, rowspan=1, padx=5, pady=5, sticky=N + E + S + W)


# Creates a top level window and widgets which are placed for the search window
# If the data input from the entry field matches a code in the shoe_list then this record is displayed

def search_shoe():
    top = Toplevel(window)
    top.title("Search")
    top.resizable(False, False)
    top.geometry("332x180")

    lbl_search = Label(top, text="Code: ")
    entry_search = Entry(top)
    search_lframe = LabelFrame(top, text="Result")
    lbl_result = Label(search_lframe, text="")

    lbl_search.grid(row=0, column=0, padx=5, pady=5, sticky=N + E + S + W, ipadx=10)
    entry_search.grid(row=0, column=1, padx=5, pady=5, sticky=N + E + S + W, ipadx=20)
    search_lframe.grid(row=2, column=0, padx=5, pady=5, sticky=N + E + S + W, columnspan=4, rowspan=3, ipadx=30)
    lbl_result.grid(row=2, column=0, padx=5, pady=5, sticky=N + E + S + W)

    def search_submit():
        found = False
        for shoe in shoe_list:

            if shoe.get_code() == entry_search.get():
                lbl_result.configure(text=f"\t\t{'Country: '} {shoe.get_country()}\n"
                                          f"\t\t{'Code: '} {shoe.get_code()}\n"
                                          f"\t\t{'Product: '} {shoe.get_product()}\n"
                                          f"\t\t{'Cost: '} {shoe.get_cost()}\n"
                                          f"\t\t{'Quantity: '} {shoe.get_quantity()}\n")
                found = True

        if not found:
            lbl_result.configure(text="\t\tNo Value Found")
            entry_search.delete(0, END)

    btn_search_submit = Button(top, text="Submit", borderwidth=2, command=search_submit)
    btn_search_submit.grid(row=0, column=2, padx=5, pady=5, sticky=N + E + S + W, ipadx=15)


# Creates a top level window and widgets for restocking a shoe
# Calls a function to find the lowest quantity of a shoe in shoe_list and displays to the GUI
# Takes the input from the entry field to add this number to the quantity of the shoe and then write this to file
def restock_shoe():
    top = Toplevel(window)
    top.title("Restock")
    top.resizable(False, False)

    lframe_restock = LabelFrame(top, text="Lowest Quantity")
    lbl_restock = Label(lframe_restock, text=f"Product: {lowest_quantity().get_product()}\n"
                                             f"Code: {lowest_quantity().get_code()}\n"
                                             f"Quantity: {lowest_quantity().get_quantity()}\n")

    lframe_restock.grid(row=0, column=0, padx=5, pady=5, sticky=N + E + S + W, columnspan=4, rowspan=3, ipadx=20)
    lbl_restock.grid(row=0, column=0, padx=5, pady=5, sticky=N + E + S + W, columnspan=4, rowspan=3, ipadx=20)

    lbl_quantity = Label(top, text="Quantity to Add:")
    entry_quantity = Entry(top)
    lbl_quantity.grid(row=3, column=0, padx=5, pady=5, sticky=N + E + S + W)
    entry_quantity.grid(row=3, column=1, padx=5, pady=5, sticky=N + E + S + W)

    def submit_restock():
        shoe = lowest_quantity()

        try:
            shoe.set_quantity(int(entry_quantity.get()))
            empty_table()
            fill_table()
            top.destroy()

            with open("inventory.txt", "w") as w:
                w.write(f"Country,Code,Product,Cost,Quantity\n")
                for shoe in shoe_list:
                    print(shoe)
                    w.write(f"{shoe}")

        except ValueError:
            print("Could Not be Added : Quantity must be numerical")
            entry_quantity.delete(0, END)

    btn_restock_quantity = Button(top, text="Submit", borderwidth=2, command=submit_restock)
    btn_restock_quantity.grid(row=4, column=0, padx=5, pady=5, sticky=N + E + S + W, columnspan=4)


# Creates a top level window and widgets for the highest quantity of shoe
# Searches shoe_list to find the highest quantity and displays to the GUI

def highest_qty():
    maximum = shoe_list[0]

    for shoe in shoe_list:
        if int(shoe.get_quantity()) > int(maximum.get_quantity()):
            maximum = shoe

    top = Toplevel(window)
    top.title("Highest Quantity")
    top.resizable(False, False)

    lframe_highest = LabelFrame(top, text="Highest Quantity")
    lbl_highest = Label(lframe_highest, text=f"Product: {maximum.get_product()}\n"
                                             f"Code: {maximum.get_code()}\n"
                                             f"Quantity: {maximum.get_quantity()}")

    lframe_highest.grid(row=0, column=0, padx=5, pady=5, ipadx=15, sticky=N + E + S + W)
    lbl_highest.grid(row=0, column=0, padx=5, pady=5, ipadx=15, sticky=N + E + S + W)


# ------------------------------------------------------------------------------------------------------------
# MAIN WINDOW

window = Tk()
window.title("Nike")
window.resizable(False, False)
style = ttk.Style()
style.theme_use("clam")

# ------------------------------------------------------------------------------------------------------------
# TABLE AND SCROLLBAR
columns = ["Country", "Code", "Product", "Cost", "Quantity", "Value"]
table = Treeview(window, columns=columns, show="headings")

table.column("0", anchor=CENTER, stretch=YES, width=100)
table.heading("0", text="Country", anchor=CENTER)
table.column("1", anchor=CENTER, stretch=YES, width=100)
table.heading("1", text="Code", anchor=CENTER)
table.column("2", anchor=CENTER, stretch=YES, width=100)
table.heading("2", text="Product", anchor=CENTER)
table.column("3", anchor=CENTER, stretch=YES, width=100)
table.heading("3", text="Cost", anchor=CENTER)
table.column("4", anchor=CENTER, stretch=YES, width=100)
table.heading("4", text="Quantity", anchor=CENTER)
table.column("5", anchor=CENTER, stretch=YES, width=100)
table.heading("5", text="Value", anchor=CENTER)

scroll_x = Scrollbar(window, orient=VERTICAL, command=table.yview)

table.grid(row=0, column=0, columnspan=4, rowspan=2, sticky=N + E + S + W, padx=5, pady=5)
scroll_x.grid(row=0, column=5, rowspan=4, columnspan=1, sticky=N + E + S + W, padx=5, pady=5)

# Calls function to read the text file and append to shoe_list
# then use this data to populate the table
read_shoes_data()
fill_table()

# ------------------------------------------------------------------------------------------------------------
# BUTTONS
btn_add = Button(window, text="Add Product", borderwidth=2, command=capture_shoe)
btn_restock = Button(window, text="Restock", borderwidth=2, command=restock_shoe)
btn_search = Button(window, text="Search", borderwidth=2, command=search_shoe)
btn_quantity = Button(window, text="Highest Quantity", borderwidth=2, command=highest_qty)

btn_add.grid(row=3, column=0, padx=5, pady=5, sticky=N + E + S + W, columnspan=1)
btn_restock.grid(row=3, column=1, padx=5, pady=5, sticky=N + E + S + W, columnspan=1)
btn_search.grid(row=3, column=2, padx=5, pady=5, sticky=N + E + S + W, columnspan=1)
btn_quantity.grid(row=3, column=3, padx=5, pady=5, sticky=N + E + S + W, columnspan=1)

# ------------------------------------------------------------------------------------------------------------

# RUN GUI

window.mainloop()
