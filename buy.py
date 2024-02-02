from tkinter import *
from tkinter import messagebox
import pandas as pd
import customtkinter
import datetime
from QR import generate_qr


def reinitiate_dict():
    global data_dict
    data_dict = {
        "Seller Name":[],
        "Serial Number":[],
        "Buying Date":[],
        "Product Category":[],
        "Product Description":[],
        "Buying Price":[],
        "MRP":[],
        "Discount":[],
    }


def save_to_inventory():
    if itemCategoryEntry.get() not in items_list:
        messagebox.showerror("Error","Select correct Product Category")
    elif itemDescriptionEntry.get()=='':
        messagebox.showerror("Error", "Please Give Product Description")
    elif ItemBuyingEntry.get() == "":
        messagebox.showerror("Error", "Please Enter Buying Price")
    elif MrpEntry.get()=='':
        messagebox.showerror("Error", "Please Enter MRP")
    elif serialNoEntry.get() == '':
        messagebox.showerror("Error","Please Enter Serial Number")
    elif ClientName.get() == "":
        messagebox.showerror("Error", "Please Enter Client name")
    else:
        reinitiate_dict()
        try:
            df = pd.read_csv('Buy.csv')
        except:
            df = pd.DataFrame(data_dict)
        data_dict["Seller Name"].append(ClientName.get())
        data_dict["Serial Number"].append(serialNoEntry.get())
        data_dict["Product Category"].append(itemCategoryEntry.get())
        data_dict["Product Description"].append(itemDescriptionEntry.get())
        data_dict["Buying Price"].append(ItemBuyingEntry.get())
        data_dict["Buying Date"].append(TodayDateEntry.get())
        data_dict["MRP"].append(MrpEntry.get())
        data_dict["Discount"].append(DiscountEntry.get())
        df = pd.concat([df,pd.DataFrame(data_dict)])
        df.to_csv('Buy.csv', index=None)
        messagebox.showinfo("Done", "Successfully Added to the inventory.")


def print_qr():
    text = serialNoEntry.get()
    # + '\n'
    # text += itemCategoryEntry.get() + '\n'
    # text += itemDescriptionEntry.get() + '\n'
    # text += MrpEntry.get() + '\n'
    # text += DiscountEntry.get() + '\n'
    if generate_qr(text):
        print("QR Generated successfully!")
    else:
        print("No QR generated!")


def clear_buying_window():
    serialNoEntry.delete(0, END)
    ClientName.delete(0,END)
    itemCategoryEntry.set('')
    itemDescriptionEntry.delete(0, END)
    ItemBuyingEntry.delete(0,END)
    MrpEntry.delete(0,END)
    DiscountEntry.delete(0,END)
    DiscountEntry.insert(0,0)


################################################################################################################################
customtkinter.set_appearance_mode("Light")

buying_window = Tk()
buying_window.geometry('2000x400')
buying_window.title("Sales")

#################################################################################################################################
HeadingLabel = Label(buying_window, text='Buying Department', font=('URW Chancery L', 30, 'bold'))
HeadingLabel.pack(fill=X)

customer_details_frame = LabelFrame(buying_window, text="Customer Details",font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
customer_details_frame.pack(fill=X)

TodayDateLabel = Label(customer_details_frame, text='Date')
TodayDateLabel.grid(row=0, column=0, padx=10)

TodayDateEntry = Entry(customer_details_frame)
TodayDateEntry.grid(row=0, column=1, padx=15, pady=10)
TodayDateEntry.insert(0,datetime.date.today().strftime("%d-%m-%Y"))

#################################################################################################################################
productFrame = LabelFrame(buying_window, text='Product Details',font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
productFrame.pack(fill=X)

IdLabel = LabelFrame(productFrame, text='Id',font=('times new roman', 15, 'bold'),)
IdLabel.grid(row=0, column=0, padx=4, pady=10)
itemIdEntry = Label(IdLabel, text='1', font=('arial', 15, 'bold'))
itemIdEntry.grid(row=0, column=0, padx=10, pady=10)

ItemClientLabel = LabelFrame(productFrame, text='Client Name',font=('times new roman', 15, 'bold'))
ItemClientLabel.grid(row=0, column=1, padx=4)
ClientName = Entry(ItemClientLabel, width=20, font=('arial', 15))
ClientName.grid(row=0, column=0, pady=8, padx=5)

SerialNoLabel = LabelFrame(productFrame, text='Serial No',font=('times new roman', 15, 'bold'))
SerialNoLabel.grid(row=0, column=2, padx=4)
serialNoEntry = Entry(SerialNoLabel, font=('arial', 15))
serialNoEntry.grid(row=0, column=0, pady=9, padx=5)

ItemCategoryLabel = LabelFrame(productFrame, text='Item Category',font=('times new roman', 15, 'bold'))
ItemCategoryLabel.grid(row=0, column=3, padx=4)
items_list = ["Refrigerator", 'Air Conditioner', 'Atta chakki', 'Fan', 'Washing Machine', 'Television', 'Purifier']
itemCategoryEntry = StringVar() 
CategoryList = customtkinter.CTkComboBox(ItemCategoryLabel, variable=itemCategoryEntry, values=items_list, width=200, font=('arial', 18))
CategoryList.grid(row=0, column=0, pady=10, padx=10)

ItemDescriptionLabel = LabelFrame(productFrame, text='Item Description',font=('times new roman', 15, 'bold'))
ItemDescriptionLabel.grid(row=0, column=4, padx=4)
itemDescriptionEntry = Entry(ItemDescriptionLabel, width=50, font=('arial', 15))
itemDescriptionEntry.grid(row=0, column=0, pady=9, padx=10)

ItemBuyingLabel = LabelFrame(productFrame, text='Buying (Rs.)',font=('times new roman', 15, 'bold'))
ItemBuyingLabel.grid(row=0, column=5, padx=4)
ItemBuyingEntry = Entry(ItemBuyingLabel, font=('arial', 15), width=10)
ItemBuyingEntry.grid(row=0, column=0, pady=9, padx=10)

ItemMrpLabel = LabelFrame(productFrame, text='MRP',font=('times new roman', 15, 'bold'))
ItemMrpLabel.grid(row=0, column=6, padx=4)
MrpEntry = Entry(ItemMrpLabel, font=('arial', 15), width=10)
MrpEntry.grid(row=0, column=0, pady=9, padx=10)

ItemDiscountLabel = LabelFrame(productFrame, text='Discount',font=('times new roman', 15, 'bold'))
ItemDiscountLabel.grid(row=0, column=7, padx=4)
DiscountEntry = Entry(ItemDiscountLabel, font=('arial', 15), width=10)
DiscountEntry.grid(row=0, column=0, pady=9, padx=10)
DiscountEntry.insert(0,0)



#################################################################################################################################
BillFrame = LabelFrame(buying_window, text='Bill Menu',font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
BillFrame.pack()

AddButton = Button(BillFrame, text='Add to Inventory', command=save_to_inventory, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
AddButton.grid(row=0, column=0, padx=10, pady=10)

QrButton = Button(BillFrame, text='Generate Qr', command=print_qr, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
QrButton.grid(row=0, column=1, padx=10, pady=10)

ClearButton = Button(BillFrame, text='Clear', command=clear_buying_window, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
ClearButton.grid(row=0, column=2, padx=10, pady=10)

def exit_window():
    buying_window.destroy()
    
ExitButton = Button(BillFrame, text='Exit', command=exit_window, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
ExitButton.grid(row=0, column=3, padx=10, pady=10)



buying_window.mainloop()