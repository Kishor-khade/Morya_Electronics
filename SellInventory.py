from tkinter import *
from tkinter import ttk
import customtkinter
import pandas as pd
import datetime
customtkinter.set_appearance_mode("Light")
from tkcalendar import Calendar
from tkinter import messagebox


def sort_treeview(tree, col, descending):
    data = [(tree.set(item, col), item) for item in tree.get_children('')]
    data.sort(reverse=descending)
    for index, (val, item) in enumerate(data):
        tree.move(item, '', index)
    tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))


def dates_check_box():
    if add_date_range.get() == 'on':
        FromDate['state'] = 'normal'
        EndDate['state'] = 'normal'
    else:
        FromDate['state'] = 'disabled'
        EndDate['state'] = 'disabled'

def find_profit():
    profit = 0
    for child in sold_products_tree.get_children(''):
        profit+=int(sold_products_tree.item(child, 'values')[-1])
    ProfitEntryLabel['text'] = profit
    clear_entry_zone()

def search_record():
    if add_date_range.get() == 'on':
        new_df = df.loc[(pd.to_datetime(df['Selling Date'], dayfirst=True)>=pd.to_datetime(FromDate.get_date(), dayfirst=True))
                        &
                        (pd.to_datetime(df['Selling Date'], dayfirst=True)<=pd.to_datetime(EndDate.get_date(), dayfirst=True))]
        if len(new_df)==0:
            messagebox.showerror('Error', f'No Items sold in between {FromDate.get_date()} and {EndDate.get_date()}')
            del new_df;clear_entry_zone()
            return
                
    if sellingDateEntry.get()!='':
        string = sellingDateEntry.get()
        try:
            pd.to_datetime(string, dayfirst=True)
        except:
            messagebox.showerror("Error", "Wrong Date Entered.\nPlease check the date once again.")
            clear_entry_zone()
            return
        try :
            new_df = new_df.loc[pd.to_datetime(new_df['Selling Date'], dayfirst=True) == pd.to_datetime(string, dayfirst=True)]
        except:
            new_df = df.loc[pd.to_datetime(df['Selling Date'], dayfirst=True) == pd.to_datetime(string, dayfirst=True)]
        if len(new_df)==0:
            messagebox.showerror('Error', f'No Items sold for date : {string}')
            del new_df;clear_entry_zone()
            return
    
    if billNoEntry.get()!='':
        billNo = billNoEntry.get()
        try:
            new_df = new_df.loc[new_df['Bill No']==billNo]
        except:
            new_df = df.loc[df['Bill No']==billNo]
        if len(new_df)==0:
            messagebox.showerror('Error', f'No Items sold with bill No : {billNo}')
            del new_df;clear_entry_zone()
            return
    
    if CategoryEntry.get()!='':
        category = CategoryEntry.get()
        try:
            new_df = new_df.loc[new_df['Product Category'] == category]
        except:
            new_df = df.loc[df['Product Category'] == category]
        if len(new_df)==0:
            messagebox.showerror('Error', f'No Items sold with category : {category}')
            del new_df;clear_entry_zone()
            return
        
    if serialNumberEntry.get()!='':
        serialNo = serialNumberEntry.get()
        try:
            new_df = new_df.loc[new_df['Serial Number'] == serialNo]
        except:
            new_df = df.loc[df['Serial Number'] == serialNo]
        if len(new_df)==0:
            messagebox.showerror('Error', f'No Items sold with Serial Number : {serialNo}')
            del new_df;clear_entry_zone()
            return
    sold_products_tree.delete(*sold_products_tree.get_children())
    for item in new_df.values:
        items = list(i for i in item)
        sold_products_tree.insert('', 'end', values=items)
    find_profit()
    del new_df
    
def clear_entry_zone():
    serialNumberEntry.delete(0,END)
    sellingDateEntry.delete(0,END)
    billNoEntry.delete(0,END)
    CategoryEntry.set('')
    

def refresh_record():
    sold_products_tree.delete(*sold_products_tree.get_children())
    for item in df.values:
        items = list(i for i in item)
        sold_products_tree.insert('', 'end', values=items)
    clear_entry_zone()
    find_profit()



def exit_window():
    sold_products_window.destroy()



sold_products_window = Tk()
sold_products_window.title("Billed Products")
sold_products_window.configure(bg='lightyellow1')

df = pd.read_csv("Sell.csv")

headingLabel = Label(sold_products_window, text='Inventory', font=('URW Chancery L', 40, 'bold'), background='indigo', pady=5, foreground='white')
headingLabel.pack(fill=X)

sold_products_tree = ttk.Treeview(sold_products_window, show="headings", height=20)
sold_products_tree["column"] = list(df.columns)
sold_products_tree["show"] = "headings"


for col in sold_products_tree["column"]:
    sold_products_tree.heading(
        col, text=col, command=lambda c=col: sort_treeview(sold_products_tree, c, False))
    if col == 'Product Description':
        sold_products_tree.column(col, width=300)
    elif col == 'Bill No':
        sold_products_tree.column(col, width=100)
    elif col in ['Buying Price', 'MRP', 'Discount']:
        sold_products_tree.column(col, width=100, anchor=E)
    elif col in ['Serial Number', 'Seller Name',]:
        sold_products_tree.column(col, width=150, anchor=W)
    else:
        sold_products_tree.column(col, width=150, anchor=CENTER)

for item in df.values:
    items = list(i for i in item)
    sold_products_tree.insert('', 'end', values=items)



sold_products_tree.pack(pady=10)


ListingFrame = LabelFrame(sold_products_window)
ListingFrame.pack()

ListingFrame1 = Frame(ListingFrame)
ListingFrame1.grid(row=0, column=0, padx=50, rowspan=2)


billNoLabel = customtkinter.CTkLabel(ListingFrame1, text='Bill No',width=100, text_color='black',font=('times new roman', 18, 'bold'))
billNoLabel.grid(row=0, column=0)
billNoEntry = customtkinter.CTkEntry(ListingFrame1, width=150, text_color='black', font=('arial', 18))
billNoEntry.grid(row=0, column=1, pady=20)

serialNumberLabel = customtkinter.CTkLabel(ListingFrame1,text='Serial No.',font=('times new roman', 18, 'bold'))
serialNumberLabel.grid(row=1, column=0)
serialNumberEntry = customtkinter.CTkEntry(ListingFrame1, width=150, text_color='black', font=('arial', 18))
serialNumberEntry.grid(row=1, column=1, pady=20)


sellingDateLabel = customtkinter.CTkLabel(ListingFrame1, text='Selling Date',font=('times new roman', 18, 'bold'))
sellingDateLabel.grid(row=0, column=2, padx=20)
sellingDateEntry = customtkinter.CTkEntry(ListingFrame1, width=150, text_color='black', font=('arial', 18))
sellingDateEntry.grid(row=0, column=3)

CategoryLabel = customtkinter.CTkLabel(ListingFrame1, text='Category',font=('times new roman', 18, 'bold'))
CategoryLabel.grid(row=1, column=2)
items_list = ["Refrigerator", 'Air Conditioner', 'Atta chakki', 'Fan', 'Washing Machine', 'Television', 'Purifier']
itemCategoryEntry = StringVar() 
CategoryEntry = customtkinter.CTkComboBox(ListingFrame1, variable=itemCategoryEntry, values=items_list, width=150, font=('arial', 18))
CategoryEntry.grid(row=1, column=3, padx=10)

ListingFrame2 = Frame(ListingFrame)
ListingFrame2.grid(row=0, column=1, columnspan=2)

add_date_range = customtkinter.StringVar(value="off")
checkbox = customtkinter.CTkCheckBox(ListingFrame2, text="Add Dates Range", command=dates_check_box,
                                     variable=add_date_range, onvalue="on", offvalue="off", font=('times new roman', 25,), checkmark_color='chartreuse4',fg_color='white', hover_color='',)
checkbox.grid(row=0, column=0, columnspan=2, pady=10)


ListingFrame3 = Frame(ListingFrame)
ListingFrame3.grid(row=1, column=1)

FromDateLabel = customtkinter.CTkLabel(ListingFrame3, text='From : ',font=('times new roman', 18, 'bold'))
FromDateLabel.grid(row=0, column=0)
FromDate = Calendar(ListingFrame3, selectmode = 'day',
               year = datetime.date.today().year, 
               month = datetime.date.today().month,
               day = datetime.date.today().day,)
FromDate.grid(row=0, column=1)



ListingFrame4 = Frame(ListingFrame)
ListingFrame4.grid(row=1, column=2,padx=50)

EndDateLabel = customtkinter.CTkLabel(ListingFrame4, text='To : ',font=('times new roman', 18, 'bold'))
EndDateLabel.grid(row=0, column=0)
EndDate = Calendar(ListingFrame4, selectmode = 'day',
               year = datetime.date.today().year, 
               month = datetime.date.today().month,
               day = datetime.date.today().day,)
EndDate.grid(row=0, column=1)

EndDate['state']='disabled'
FromDate['state'] = 'disabled'



thirdFrame = Frame(sold_products_window, background='lightyellow1')
thirdFrame.pack()

BtnFrame = Frame(thirdFrame, background='lightyellow1')
BtnFrame.grid(row=0, column=0, pady=10)

SearchButton = Button(BtnFrame, text='Search', font=('times new roman', 18, 'bold'), border=3, command=search_record)
SearchButton.grid(row=0, column=0, padx=20)
ExitButton = Button(BtnFrame, text='Exit', font=('times new roman', 18, 'bold'), border=3, command=exit_window)
ExitButton.grid(row=0, column=1, padx=20)
RefreshButton = Button(BtnFrame, text='Refresh', font=('times new roman', 18, 'bold'), border=3, command=refresh_record)
RefreshButton.grid(row=0, column=2, padx=20)

ProfitFrame = LabelFrame(thirdFrame, background='lightyellow1', width=50, border=3)
ProfitFrame.grid(row=0, column=1, padx=50, pady=10)

ProfitLabel = Label(ProfitFrame, text='Total Profit', font=('times new roman', 18, 'bold'), background='lightyellow1', )
ProfitLabel.grid(row=0, column=0,)

ProfitEntryLabel = Label(ProfitFrame, text='0', font=('arial', 18, 'bold'),border=3, padx=5, pady=5, relief='ridge', width=10)
ProfitEntryLabel.grid(row=0, column=1, padx=20, pady=10)


find_profit()

sold_products_window.mainloop()





'''
def search_record():
    new_items = []
    if add_date_range.get() == 'on':
        new_df = df.loc[(pd.to_datetime(df['Selling Date'], dayfirst=True)>=pd.to_datetime(FromDate.get_date(), dayfirst=True))
                        &
                        (pd.to_datetime(df['Selling Date'], dayfirst=True)<=pd.to_datetime(EndDate.get_date(), dayfirst=True))]
        if len(new_df)>0:
            for item in new_df.values:
                items = tuple(i for i in item)
                new_items.append(items)
        else:
            messagebox.showerror('Error', f'No Items sold in between {FromDate.get_date()} and {EndDate.get_date()}')
            del new_items, new_df
            return
                
    if sellingDateEntry.get()!='':
        string = sellingDateEntry.get()
        new_df = df.loc[pd.to_datetime(df['Selling Date'], dayfirst=True) == pd.to_datetime(string, dayfirst=True)]
        if len(new_df)>0:
            for item in new_df.values:
                items = tuple(i for i in item)
                new_items.append(items)
        else:
            messagebox.showerror('Error', f'No Items sold for date : {string}')
            del new_items, new_df
            return
    
    if billNoEntry.get()!='':
        billNo = billNoEntry.get()
        new_df = df.loc[df['Bill No']==billNo]
        if len(new_df)>0:
            for item in new_df.values:
                items = tuple(i for i in item)
                new_items.append(items)
        else:
            messagebox.showerror('Error', f'No Items sold with bill No : {billNo}')
            del new_items, new_df
            return
    
    if CategoryEntry.get()!='':
        category = CategoryEntry.get()
        new_df = df.loc[df['Product Category'] == category]
        if len(new_df)>0:
            for item in new_df.values:
                items = tuple(i for i in item)
                new_items.append(items)
        else:
            messagebox.showerror('Error', f'No Items sold with category : {category}')
            del new_items, new_df
            return
    # print(set(new_items))
    # print(new_items)
    tree.delete(*tree.get_children())
    new_items = list(set(new_items))
    for item in new_items:
        tree.insert('', 'end', values=item)
    find_profit()
    del new_items, new_df
    '''