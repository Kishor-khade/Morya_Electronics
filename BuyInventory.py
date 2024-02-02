from tkinter import *
from tkinter import ttk, messagebox, font
import customtkinter
import pandas as pd
from QR import generate_qr

def clear_product_area():
    SerialNumberEntry.delete(0,END)
    SellerNameEntry.delete(0,END)
    BuyingDateEntry.delete(0,END)
    ItemCategoryEntry.set('')
    ItemDescriptionEntry.delete(0,END)
    ItemBuyingEntry.delete(0,END)
    ItemMrpEntry.delete(0,END)
    ItemDiscountEntry.delete(0,END)


selected = ''
def select_record():
    global selected
    selected = tree.focus()
    if selected != '':
        values = tree.item(selected, 'values')
        clear_product_area()
        SellerNameEntry.insert(0, values[0])
        SerialNumberEntry.insert(0, values[1])
        BuyingDateEntry.insert(0, values[2])
        ItemCategoryEntry.set(values[3])
        ItemDescriptionEntry.insert(0, values[4])
        ItemBuyingEntry.insert(0, values[5])
        ItemMrpEntry.insert(0, values[6])
        ItemDiscountEntry.insert(0, values[7])
    else:
        messagebox.showerror("Error", "No Data row is selected!")    


def delete_record():
    global selected
    selected = tree.focus()
    if selected != '':
        if not messagebox.askokcancel("", 'Do you really want to delete?'):
            return
        values = tree.item(selected, 'values')
        try:
            df = pd.read_csv('Buy.csv')
            print(df)
            df.drop(index=df[df['Serial Number']==values[1]].index, inplace=True)
            print(df)
            selected_item = tree.selection()[0]
            tree.delete(selected_item)
            df.to_csv('Buy.csv', index=False)
        except:
            messagebox.showerror("Error", "Found Error in the code.....")
            return
        messagebox.showinfo("Done", "Record Deleted from Inventory Sucessfully!")
    else:
        messagebox.showerror("Error", "No Data row is selected!")

def get_qr():
    global selected
    selected = tree.focus()
    if selected != '':
        values = tree.item(selected, 'values')
        if generate_qr(values[1]):
            messagebox.showinfo("Successfull", "Generated Qr Sucessfully")
        else:
            messagebox.showerror("Error", "Found Error in the code.....")
    else:
        messagebox.showerror("Error", "No Data row is selected!")

def search_record():
    df = pd.read_csv('Buy.csv')
    new_df = pd.DataFrame()
    if SellerNameEntry.get()=='' and SerialNumberEntry.get()=='' and BuyingDateEntry.get()=='' and ItemCategoryEntry.get()=='' and ItemDescriptionEntry.get()=='' and ItemBuyingEntry.get()=='' and ItemMrpEntry.get()=='':
        messagebox.showerror('Error', "Please Enter any value to search!")
        return
    if SellerNameEntry.get()!='':
        seller_name = SellerNameEntry.get()
        new_df = df[df['Seller Name'].str.contains(seller_name, case=False)]
        
    if SerialNumberEntry.get()!='':
        serial_no = SerialNumberEntry.get()
        if len(new_df)>0:
            new_df = new_df[new_df['Serial Number'].str.contains(serial_no, case=False)]
        else:
            new_df = df[df['Serial Number'].str.contains(serial_no, case=False)]
            
    if BuyingDateEntry.get()!='':
        buying_date = BuyingDateEntry.get()
        if len(new_df)>0:
            new_df = new_df[new_df['Buying Date'].str.contains(buying_date, case=False)]
        else:
            new_df = df[df['Buying Date'].str.contains(buying_date, case=False)]
            
    if ItemCategoryEntry.get()!='':
        category = ItemCategoryEntry.get()
        if len(new_df)>0:
            new_df = new_df[new_df['Product Category'].str.contains(category, case=False)]
        else:
            new_df = df[df['Product Category'].str.contains(category, case=False)]
            
    if ItemDescriptionEntry.get()!='':
        description = ItemDescriptionEntry.get()
        if len(new_df)>0:
            new_df = new_df[new_df['Product Description'].str.contains(description, case=False)]
        else:
            new_df = df[df['Product Description'].str.contains(description, case=False)]
            
    if ItemBuyingEntry.get()!='':
        buying_price = int(ItemBuyingEntry.get())
        if len(new_df)>0:
            new_df = new_df[[True if (i==buying_price) else False for i in new_df['Buying Price']]]
        else:
            new_df = df[[True if (i==buying_price) else False for i in df['Buying Price']]]
            
    if ItemMrpEntry.get()!='':
        mrp = int(ItemMrpEntry.get())
        if len(new_df)>0:
            new_df = new_df[[True if (i==mrp) else False for i in new_df['MRP']]]
        else:
            new_df = df[[True if (i==mrp) else False for i in df['MRP']]]
    tree.delete(*tree.get_children())
    for item in new_df.values:
        items = list(i for i in item)
        tree.insert('', 'end', values=items)
    
def refresh_record():
    tree.delete(*tree.get_children())
    for item in df.values:
        items = list(i for i in item)
        tree.insert('', 'end', values=items)

def update_record():
    pass


def sort_treeview(tree, col, descending):
    data = [(tree.set(item, col), item) for item in tree.get_children('')]
    data.sort(reverse=descending)
    for index, (val, item) in enumerate(data):
        tree.move(item, '', index)
    tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))


inventory_window = Tk()
inventory_window.title("Stock Inventory ")
inventory_window.geometry("1400x960")
inventory_window.configure(bg='lightyellow1')

df = pd.read_csv("Buy.csv")
# df.drop(columns=['Sold Price', 'Selling Date', 'Bill No'], inplace=True)


headingLabel = Label(inventory_window, text='Inventory', font=('URW Chancery L', 40, 'bold'), background='indigo', pady=5, foreground='white')
headingLabel.pack(fill=X)

tree = ttk.Treeview(inventory_window, show="headings", height=30)
tree["column"] = list(df.columns)
tree["show"] = "headings"

for col in tree["column"]:
    tree.heading(
        col, text=col, command=lambda c=col: sort_treeview(tree, c, False))
    if col == 'Product Description':
        tree.column(col, width=300)
    elif col in ['Buying Price', 'MRP', 'Discount']:
        tree.column(col, width=100, anchor=E)
    elif col in ['Serial Number', 'Seller Name', 'Buying Date']:
        tree.column(col, width=150, anchor=W)
    else:
        tree.column(col, width=200, anchor=CENTER)

for item in df.values:
    items = list(i for i in item)
    tree.insert('', 'end', values=items)

tree.pack(pady=10)

buttonsFrame1 = Frame(inventory_window, background='lightyellow1')
buttonsFrame1.pack()

selectButton = Button(buttonsFrame1, text="Select",command=select_record, background='gray80', activebackground='gray60', font=('times new roman', 15))
selectButton.grid(row=0, column=0,padx=10)
clearButton = Button(buttonsFrame1, text="Delete", command=delete_record, background='gray80', activebackground='gray60', font=('times new roman', 15))
clearButton.grid(row=0, column=1)
getQRButton = Button(buttonsFrame1, text="Get QR", command=get_qr, background='gray80', activebackground='gray60', font=('times new roman', 15))
getQRButton.grid(row=0, column=2, padx=10)
getQRButton = Button(buttonsFrame1, text="Refresh data", command=refresh_record, background='gray80', activebackground='gray60', font=('times new roman', 15))
getQRButton.grid(row=0, column=3)


entryFrame = Frame(inventory_window, border=5, relief='groove', background='lightyellow1')
entryFrame.pack(pady=10, anchor=CENTER)

SellerNameLabel = Label(entryFrame, text="Seller Name", font=('times new roman', 15), background='lightyellow1')
SellerNameLabel.grid(row=0, column=0)
SellerNameEntry = Entry(entryFrame, font=('arial', 13))
SellerNameEntry.grid(row=1, column=0)


SerialNumberLabel = Label(entryFrame, text="Serial No.", font=('times new roman', 15), background='lightyellow1')
SerialNumberLabel.grid(row=0, column=1)
SerialNumberEntry = Entry(entryFrame, font=('arial', 13))
SerialNumberEntry.grid(row=1, column=1)


BuyingDateLabel = Label(entryFrame, text="Buying Date", font=('times new roman', 15), background='lightyellow1')
BuyingDateLabel.grid(row=0, column=2)
BuyingDateEntry = Entry(entryFrame, font=('arial', 13))
BuyingDateEntry.grid(row=1, column=2)


itemCategoryLabel = Label(entryFrame, text="Category", font=('times new roman', 15), background='lightyellow1')
itemCategoryLabel.grid(row=0, column=3)


items_list = ["Random", "Low HP Pool",
              "Medium HP Pool", "High HP Pool", "Extreme HP Pool"]
customtkinter.set_appearance_mode("Light")
ItemCategoryEntry = StringVar()
ItemCategoryComboBoxEntry = customtkinter.CTkComboBox(entryFrame,
                                                      variable=ItemCategoryEntry,  # set variable in combobox
                                                      values=items_list, width=200, font=('arial', 15))
ItemCategoryComboBoxEntry.grid(row=1, column=3, padx=10)


ItemDescriptionLabel = Label(entryFrame, text="Description", font=('times new roman', 15), background='lightyellow1')
ItemDescriptionLabel.grid(row=0, column=4)
ItemDescriptionEntry = Entry(entryFrame, width=40, font=('arial', 13))
ItemDescriptionEntry.grid(row=1, column=4, padx=10)


ItemBuyingLabel = Label(entryFrame, text="Buying Price", font=('times new roman', 15), background='lightyellow1')
ItemBuyingLabel.grid(row=2, column=0)
ItemBuyingEntry = Entry(entryFrame, font=('arial', 13))
ItemBuyingEntry.grid(row=3, column=0, padx=10)


ItemMrpLabel = Label(entryFrame, text="MRP", font=('times new roman', 15), background='lightyellow1')
ItemMrpLabel.grid(row=2, column=1, padx=10)
ItemMrpEntry = Entry(entryFrame, font=('arial', 13))
ItemMrpEntry.grid(row=3, column=1, padx=10)


ItemDiscountLabel = Label(entryFrame, text="Discount", font=('times new roman', 15), background='lightyellow1')
ItemDiscountLabel.grid(row=2, column=2, padx=10)
ItemDiscountEntry = Entry(entryFrame, font=('arial', 13))
ItemDiscountEntry.grid(row=3, column=2, padx=10, pady=5)


buttonsFrame = Frame(inventory_window, background='lightyellow1')
buttonsFrame.pack()

def exit_window():
    inventory_window. destroy()

searchButton = Button(buttonsFrame, text="Search", command=search_record, font=('times new roman',18), foreground='black', relief='raised', border=3, background='gray80', activebackground='gray60')
searchButton.grid(row=0, column=1, padx=10)
# updateButton = Button(buttonsFrame, text="Update", command=update_record, font=('times new roman',18), foreground='black', relief='raised', border=3, background='gray80', activebackground='gray60')
# updateButton.grid(row=0, column=2, padx=10)
clearButton = Button(buttonsFrame, text="Clear", command=clear_product_area, font=('times new roman',18), foreground='black', relief='raised', border=3, background='gray80', activebackground='gray60')
clearButton.grid(row=0, column=3, padx=10)
exitButton = Button(buttonsFrame, text="Exit", command=exit_window, font=('times new roman',18),foreground='black', relief='raised', border=3, background='gray80', activebackground='gray60')
exitButton.grid(row=0, column=4, padx=10)


inventory_window.mainloop()
