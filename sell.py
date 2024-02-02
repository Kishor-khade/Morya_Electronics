from tkinter import *
from tkinter import ttk, messagebox, font
import customtkinter
import datetime
from doc_gen import generate_selling_bill
from QR import decode_qr
import pandas as pd
from num2words import num2words


global invoice_items, total
invoice_items = []
total = 0


selling_dictionary = {
    'Bill No':[],
    'Seller Name':[],
    'Customer Name':[],
    'Buying Date':[],
    'Selling Date':[],
    'Serial Number':[],
    'Product Category':[],
    'Product Description':[],
    'Buying Price':[],
    'Selling Price':[],
    'Profit':[]
}

def add_to_database():
    try:
        sell_df = pd.read_csv('Sell.csv')
    except:
        sell_df = pd.DataFrame()
    buy_df = pd.read_csv('Buy.csv')
    if buy_df.shape == (0,0):
        messagebox.showinfo("Error", "0 Products in inventory.")
    indexes = []
    for item in invoice_items:
        temp_df = buy_df.loc[buy_df['Serial Number']==item[1]]
        if temp_df.size==0:
            messagebox.showerror("Not Found", f"SERIAL NO : {item[1]} \nnot found int he database \n\nDescription : {item[3]}")
            return False
        index = temp_df.index[0]
        indexes.append(index)
        selling_dictionary['Bill No'].append(billNoEntry.get())
        selling_dictionary['Seller Name'].append(temp_df['Seller Name'].values[0])
        selling_dictionary['Customer Name'].append(NameEntry.get())
        selling_dictionary['Buying Date'].append(temp_df['Buying Date'].values[0])
        selling_dictionary['Selling Date'].append(TodayDateEntry.get())
        selling_dictionary['Serial Number'].append(temp_df['Serial Number'].values[0])
        selling_dictionary['Product Category'].append(temp_df['Product Category'].values[0])
        selling_dictionary['Product Description'].append(temp_df['Product Description'].values[0])
        selling_dictionary['Buying Price'].append(temp_df['Buying Price'].values[0])
        selling_dictionary['Selling Price'].append(item[-1])
        selling_dictionary['Profit'].append(int(item[-1])-int(temp_df['Buying Price'].values[0]))
    temp_df = pd.DataFrame(selling_dictionary)
    sell_df = pd.concat([sell_df, temp_df])
    sell_df.to_csv('Sell.csv', index=False)
    buy_df.drop(index=indexes, inplace=True)
    buy_df.reset_index(inplace=True, drop=True)
    buy_df.to_csv('Buy.csv', index=False)
    return True

def refresh_date():
    TodayDateEntry.delete(0, END)
    TodayDateEntry.insert(0,datetime.date.today().strftime("%d-%m-%Y"))

def clear_product_area():
    IdEntry.delete(0,END)
    ItemserialNoEntry.delete(0,END)
    ItemCategoryEntry.set('')
    ItemDescriptionEntry.delete(0,END)
    ItemMrpEntry.delete(0,END)
    ItemDiscountEntry.delete(0,END)


def clear_all_details():
    global invoice_items
    invoice_items = []
    NameEntry.delete(0,END)
    NumberEntry.delete(0,END)
    GstNumberEntry.delete(0,END)
    TodayDateEntry.delete(0,END)
    TodayDateEntry.insert(0,datetime.date.today().strftime("%d-%m-%Y"))
    billNoEntry.delete(0,END)
    AddressEntry.delete(0, END)
    tree.delete(*tree.get_children())
    TotalAmtEntry.delete(0,END)
    DiscountEntry.delete(0,END)
    DiscountEntry.insert(0,0)
    CgstEntry.delete(0,END)
    CgstEntry.insert(0,9)
    SgstEntry.delete(0,END)
    SgstEntry.insert(0,9)
    TotalTaxableEntry.delete(0,END)
    CalculatedCgstEntry.delete(0,END)
    CalculatedSgstEntry.delete(0,END)
    TotalPayableEntry['text'] = '0.00'
    BankNameEntry.delete(0,END)
    AccountNumberEntry.delete(0, END)
    IfscCodeEntry.delete(0, END)
    DueDateEntry.delete(0, END)
    clear_product_area()


def add_item():
    if IdEntry.get() == '':
        messagebox.showerror("Error", "Please Enter ID")
    elif ItemserialNoEntry.get()=='':
        messagebox.showerror("Error", "Please Enter Serial No")
    elif ItemCategoryEntry.get()=='':
        messagebox.showerror("Error", "Please Select Category")
    elif ItemDescriptionEntry.get()=='':
        messagebox.showerror("Error", "Please Enter Product Description")
    elif ItemMrpEntry.get()=='':
        messagebox.showerror("Error", "Please Enter MRP")
    else:
        mrp = int(ItemMrpEntry.get())
        discount = int(ItemDiscountEntry.get())
        total = mrp-discount
        tree.insert('', END, 
                    values=(
                        IdEntry.get(),
                        ItemserialNoEntry.get(),
                        ItemCategoryEntry.get(),
                        ItemDescriptionEntry.get(),
                        mrp,
                        discount, 
                        total) 
                        )
        clear_product_area()

selected = ''
def select_record():
    global selected, payment_method
    selected = tree.focus()
    if selected != '':
        values = tree.item(selected, 'values')
        clear_product_area()
        IdEntry.insert(0,values[0])
        ItemserialNoEntry.insert(0, values[1])
        ItemCategoryEntry.set(values[2])
        ItemDescriptionEntry.insert(0,values[3])
        ItemMrpEntry.insert(0,values[4])
        ItemDiscountEntry.insert(0,values[5])
    else:
        messagebox.showerror("Error", "No Data row is selected!")

def update_record():
    global selected
    if selected !='':    
        tree.item(selected, text="", values=(IdEntry.get(),ItemserialNoEntry.get(),ItemCategoryEntry.get(),ItemDescriptionEntry.get(),ItemMrpEntry.get(),ItemDiscountEntry.get(),int(ItemMrpEntry.get())-int(ItemDiscountEntry.get())))
        clear_product_area()
        selected = ''
    else:
        messagebox.showerror("Error", "Please Select record first \n then update it")


def delete_record():
    try:
        selected_item = tree.selection()[0] ## get selected item
        tree.delete(selected_item)
    except:
        messagebox.showerror("Error", "No Record was selected")


def QrScan():
    buy_df = pd.read_csv('Buy.csv')
    serial_no = decode_qr()
    temp_df = buy_df.loc[buy_df['Serial Number']==serial_no]
    if temp_df.size>0:
        ItemserialNoEntry.delete(0,END)
        ItemserialNoEntry.insert(0,serial_no)
        ItemCategoryEntry.set(temp_df.values[0][3])
        ItemDescriptionEntry.delete(0,END)
        ItemDescriptionEntry.insert(0,temp_df.values[0][4])
        ItemMrpEntry.delete(0,END)
        ItemMrpEntry.insert(0,temp_df.values[0][6])
        ItemDiscountEntry.delete(0,END)
        ItemDiscountEntry.insert(0,temp_df.values[0][7])
    else:
        messagebox.showwarning("Error","Product Not Found")
    return


def all_product_sum():
    global invoice_items
    invoice_items = []
    temp_total = 0.0
    for child in tree.get_children():
        invoice_items.append(tree.item(child, 'values'))
        temp_total += float(tree.item(child, 'values')[6])
    return temp_total


def find_total():
    global total
    # Calculate Total form products
    total = all_product_sum()
    TotalAmtEntry.delete(0,END)
    TotalAmtEntry.insert(0, f"{total:.2f}")
    # Calculate Taxable amount
    new_total = total-int(DiscountEntry.get())
    TotalTaxableEntry.delete(0, END)
    TotalTaxableEntry.insert(0,f"{new_total:.2f}")
    # Calculate csgt and sgst
    calc_cgst = new_total*float(CgstEntry.get())/100
    calc_sgst = new_total*float(SgstEntry.get())/100
    CalculatedCgstEntry.delete(0,END)
    CalculatedCgstEntry.insert(0, calc_cgst)
    CalculatedSgstEntry.delete(0, END)
    CalculatedSgstEntry.insert(0, calc_sgst)
    # Calculate Grand Total Amount
    new_total += calc_cgst+ calc_sgst
    TotalPayableEntry['text'] = new_total


def get_payment_mode():
    if CashCheckVar.get()==1:
        return "Cash"
    elif CreditCheckVar.get()==1:
        return "Credit"
    elif OnlineCheckVar.get()==1:
        return "Online"
    return

def get_bank_details():
    if CreditCheckVar.get()==1:
        string = ''
        string += f"Bank : {BankNameEntry.get()}\n"
        string += f"A/c No : {AccountNumberEntry.get()}\n"
        string += f"IFSC : {IfscCodeEntry.get()}\n"
        string += f"Due : {DueDateEntry.get()}"
        return string
    else:
        return ''

def create_bill():
    if NameEntry.get()=='':
        return messagebox.showerror("Error", "Please! Enter Customer Name. ")
    elif NumberEntry.get()=='':
        return messagebox.showerror("Error", "Please! Enter Customer Phone number. ")
    elif AddressEntry.get()=='':
        return messagebox.showerror("Error", "Please! Enter Customer address. ")
    elif TodayDateEntry.get()=='':
        return messagebox.showerror("Error", "Please! click once Refresh date button. ")
    elif TotalAmtEntry.get()=='':
        return messagebox.showerror("Error", "Please! Find the total First. ")
    elif [CreditCheckVar.get(),CashCheckVar.get(),OnlineCheckVar.get()] == [0,0,0]:
        messagebox.showerror('Error', "Please chose payment method")
    elif not add_to_database():
        return
    else:
        total_items = 0
        for child in tree.get_children():
            total_items+=1
        detail_dict = {
        'name': NameEntry.get(),
        'address':AddressEntry.get(),
        'number':NumberEntry.get(),
        'gst_number':GstNumberEntry.get(),
        'bill_no':billNoEntry.get(),
        'today_date':TodayDateEntry.get(),
        'payment_mode':get_payment_mode(),
        'bank_details':get_bank_details(),
        'total':TotalAmtEntry.get(),
        'total_discount':DiscountEntry.get(),
        'taxable_amt':TotalTaxableEntry.get(),
        'cgst':CalculatedCgstEntry.get(),
        'sgst':CalculatedSgstEntry.get(),
        'cgst_per':CgstEntry.get(),
        'sgst_per':SgstEntry.get(),
        'round_off':int(float(TotalPayableEntry['text']))-float(TotalPayableEntry['text']),
        'grand_total':int(float(TotalPayableEntry['text'])),
        'amount_in_words':num2words(int(float(TotalPayableEntry['text']))),
        'total_items':total_items,
        }
        generate_selling_bill(invoice_list=invoice_items, detail_dict=detail_dict)
        
        clear_content = messagebox.askokcancel('Clear', "Do you want to clear all the content on the screen?")
        if clear_content:
            clear_all_details()
        else:
            if messagebox.askokcancel("Clear", "Do you want to clear the Product details on the screen?"):
                clear_product_area()


def payment_clciked():
    if [OnlineCheckVar.get(),CashCheckVar.get(),CreditCheckVar.get()] in [[1,1,1], [0,0,0]]:
        OnlinePaymentButton['state'] = 'normal'
        CashPaymentButton['state'] = 'normal'
        CreditPaymentButton['state'] = 'normal'
        BankNameEntry['state'] = 'disabled';AccountNumberEntry['state'] = 'disabled'
        IfscCodeEntry['state'] = 'disabled';DueDateEntry['state'] = 'disabled'
    elif OnlineCheckVar.get()==1:
        OnlinePaymentButton['state'] = 'normal'
        CashPaymentButton['state'] = 'disabled'
        CreditPaymentButton['state'] = 'disabled'
        BankNameEntry['state'] = 'disabled';AccountNumberEntry['state'] = 'disabled'
        IfscCodeEntry['state'] = 'disabled';DueDateEntry['state'] = 'disabled'
    elif CashCheckVar.get()==1:
        OnlinePaymentButton['state'] = 'disabled'
        CashPaymentButton['state'] = 'normal'
        CreditPaymentButton['state'] = 'disabled'
        BankNameEntry['state'] = 'disabled';AccountNumberEntry['state'] = 'disabled'
        IfscCodeEntry['state'] = 'disabled';DueDateEntry['state'] = 'disabled'
    elif CreditCheckVar.get()==1:
        OnlinePaymentButton['state'] = 'disabled'
        CashPaymentButton['state'] = 'disabled'
        CreditPaymentButton['state'] = 'normal'
        BankNameEntry['state'] = 'normal';AccountNumberEntry['state'] = 'normal'
        IfscCodeEntry['state'] = 'normal';DueDateEntry['state'] = 'normal'
        messagebox.showinfo("Process", "For Credit, Please Enter Bank details")


#################################################################################################################################
customtkinter.set_appearance_mode("Light")

selling_window = Tk()
selling_window.geometry('1730x880+0+0')
selling_window.title("Sales")
# new_root.attributes('-topmost',True)

#################################################################################################################################
HeadingLabel = Label(selling_window, text='Selling Department', font=('URW Chancery L', 50, 'bold'), relief='raised', border=5)
HeadingLabel.pack(fill=X, padx=10,pady=5)

#################################################################################################################################
customer_details_frame = LabelFrame(selling_window, text="Customer Details",font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
customer_details_frame.pack(fill=X, padx=10)

billNoLabel = Label(customer_details_frame, text='Bill No')
billNoLabel.grid(row=0,column=0, padx=10, pady=10)

billNoEntry = Entry(customer_details_frame)
billNoEntry.grid(row=0, column=1, padx=15)

NameLabel = Label(customer_details_frame, text='Name')
NameLabel.grid(row=0, column=2, padx=10)

NameEntry = Entry(customer_details_frame)
NameEntry.grid(row=0,column=3, padx=15)

NumberLabel = Label(customer_details_frame, text='Number',)
NumberLabel.grid(row=0, column=4, padx=10)

NumberEntry = Entry(customer_details_frame)
NumberEntry.grid(row=0, column=5, padx=15)

GstNumberLabel = Label(customer_details_frame, text='Customer Gst in : ')
GstNumberLabel.grid(row=0, column=6, padx=10)

GstNumberEntry = Entry(customer_details_frame)
GstNumberEntry.grid(row=0, column=7, padx=15)

TodayDateLabel = Label(customer_details_frame, text='Date')
TodayDateLabel.grid(row=0, column=8, padx=10)

TodayDateEntry = Entry(customer_details_frame)
TodayDateEntry.grid(row=0, column=9)
TodayDateEntry.insert(0,datetime.date.today().strftime("%d-%m-%Y"))

refresh_image = PhotoImage(file='refresh.png')
DateRefreshButton = Button(customer_details_frame, image=refresh_image, command=refresh_date)
DateRefreshButton.grid(row=0, column=10, padx=5, pady=10)

AddressLabel = Label(customer_details_frame, text='Address')
AddressLabel.grid(row=1, column=0, padx=10)

AddressEntry = Entry(customer_details_frame, width=90)
AddressEntry.grid(row=1, column=1, pady=10, columnspan=5)

#################################################################################################################################
productFrame = LabelFrame(selling_window, text='Product Details',font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
productFrame.pack(fill=X, padx=10)


IdLabel = LabelFrame(productFrame, text='Id',font=('times new roman', 15, 'bold'),)
IdLabel.grid(row=0, column=0, padx=4, pady=10)
IdEntry = Entry(IdLabel, font=('arial', 15), width=3)
IdEntry.grid(row=0, column=0, padx=10, pady=10)


ItemQrLabel = LabelFrame(productFrame, text='QR Entry',font=('times new roman', 15, 'bold'))
ItemQrLabel.grid(row=0, column=1, padx=4)
ItemQrScan = Button(ItemQrLabel, text='Scan', width=7, command=QrScan)
ItemQrScan.grid(row=0, column=0, pady=8, padx=5)


ItemSerialNoLabel = LabelFrame(productFrame, text='Serial No',font=('times new roman', 15, 'bold'))
ItemSerialNoLabel.grid(row=0, column=2, padx=4)
ItemserialNoEntry = Entry(ItemSerialNoLabel, font=('arial', 15))
ItemserialNoEntry.grid(row=0, column=0, pady=9, padx=5)


ItemCategoryLabel = LabelFrame(productFrame, text='Item Category',font=('times new roman', 15, 'bold'))
ItemCategoryLabel.grid(row=0, column=3, padx=4)
items_list = ["Random","Low HP Pool", "Medium HP Pool", "High HP Pool", "Extreme HP Pool"]
ItemCategoryEntry = StringVar() #initialize variable
ItemCategoryComboBoxEntry = customtkinter.CTkComboBox(ItemCategoryLabel,
                                                 variable=ItemCategoryEntry, #set variable in combobox
                                                 values=items_list, width=200, font=('arial', 15))
ItemCategoryComboBoxEntry.grid(row=0, column=0, pady=10, padx=10)


ItemDescriptionLabel = LabelFrame(productFrame, text='Item Description',font=('times new roman', 15, 'bold'))
ItemDescriptionLabel.grid(row=0, column=4, padx=4)
ItemDescriptionEntry = Entry(ItemDescriptionLabel, font=('arial', 15), width=30)
ItemDescriptionEntry.grid(row=0, column=0, pady=9, padx=10)


ItemMrpLabel = LabelFrame(productFrame, text='MRP',font=('times new roman', 15, 'bold'))
ItemMrpLabel.grid(row=0, column=5, padx=4)
ItemMrpEntry = Entry(ItemMrpLabel, font=('arial', 15), width=10)
ItemMrpEntry.grid(row=0, column=0, pady=9, padx=10)


ItemDiscountLabel = LabelFrame(productFrame, text='Discount',font=('times new roman', 15, 'bold'))
ItemDiscountLabel.grid(row=0, column=6, padx=4)
ItemDiscountEntry = Entry(ItemDiscountLabel, font=('arial', 15), width=10)
ItemDiscountEntry.grid(row=0, column=0, pady=9, padx=10)
ItemDiscountEntry.insert(0,0)


AddItemButton = Button(productFrame, text="➕ Add Item", command=add_item, border=3,)
AddItemButton.grid(row=1, column=6)


columns = ('id', 'serial_no', 'item_cat', 'item_desc', 'item_mrp', 'item_discount', 'item_total')
tree = ttk.Treeview(productFrame, columns=columns, show="headings")

tree.column('id', width=30, anchor=CENTER)
tree.column('serial_no', width=200, anchor=CENTER)
tree.column('item_cat', width=200, anchor=CENTER)
tree.column('item_desc', width=400, anchor=CENTER)
tree.column('item_mrp', width=150, anchor=E)
tree.column('item_discount', width=150, anchor=E)
tree.column('item_total', width=150, anchor=E)

tree.heading('id', text="ID")
tree.heading('serial_no', text="Serial Number")
tree.heading('item_cat', text="Category")
tree.heading('item_desc', text="Description")
tree.heading('item_mrp', text="MRP")
tree.heading('item_discount', text="Product Discount")
tree.heading('item_total', text="Total")

tree.grid(row=2, column=0, columnspan=7, padx=10, pady=10)

style = ttk.Style(tree)
fnt=font.Font(size=12, family='arial')
style.configure('Treeview', rowheight=30)
style.configure('Treeview', font=fnt)


delete_record_button = Button(productFrame, text='Delete Record', command=delete_record)
delete_record_button.grid(row=3, column=4, pady=10,sticky=E, padx=10)

select_record_button = Button(productFrame, text="Select Record", command=select_record)
select_record_button.grid(row=3, column=5,pady=10)

update_record_button = Button(productFrame, text="Update Record", command=update_record)
update_record_button.grid(row=3, column=6, pady=10)


##################################################################################################################################
TotalMenuFrame = LabelFrame(productFrame, text="Total Menu",font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
TotalMenuFrame.grid(row=0, column=7, rowspan=4)


TotalAmtLabel = Label(TotalMenuFrame, text="Total Amt", font=('times new roman', 15, 'bold'))
TotalAmtLabel.grid(row=0,column=0, pady=10, padx=10)
TotalAmtEntry = Entry(TotalMenuFrame, font=('arial', 15), width=10)
TotalAmtEntry.grid(row=0, column=1, pady=15, padx=10)

DiscountLabel = Label(TotalMenuFrame, text="Extra Discount", font=('times new roman', 15, 'bold'))
DiscountLabel.grid(row=1, column=0, pady=10, padx=10)
DiscountEntry = Entry(TotalMenuFrame, font=('arial', 15), width=10)
DiscountEntry.grid(row=1, column=1, pady=15, padx=10)
DiscountEntry.insert(0, 0)

CgstLabel = Label(TotalMenuFrame, text='CGST (%)', font=('times new roman', 15, 'bold'))
CgstLabel.grid(row=2, column=0, padx=10)
CgstEntry = Entry(TotalMenuFrame, font=('arial', 15), width=10)
CgstEntry.grid(row=2, column=1, pady=15, padx=10)
CgstEntry.insert(0,9)

SgstLabel = Label(TotalMenuFrame, text='SGST (%)', font=('times new roman', 15, 'bold'))
SgstLabel.grid(row=3, column=0, padx=10)
SgstEntry = Entry(TotalMenuFrame, font=('arial', 15), width=10)
SgstEntry.grid(row=3, column=1, pady=15, padx=10)
SgstEntry.insert(0,9)

TotalTaxableLabel = Label(TotalMenuFrame, text='Total taxable', font=('times new roman', 15, 'bold'))
TotalTaxableLabel.grid(row=4, column=0, padx=10)
TotalTaxableEntry = Entry(TotalMenuFrame, font=('arial', 15, 'bold'), width=10)
TotalTaxableEntry.grid(row=4, column=1, pady=15, padx=10)

CalculatedCgstLabel = Label(TotalMenuFrame, text='CGST (Rs)', font=('times new roman', 15, 'bold'))
CalculatedCgstLabel.grid(row=5, column=0, padx=10)
CalculatedCgstEntry = Entry(TotalMenuFrame, font=('arial', 15), width=10)
CalculatedCgstEntry.grid(row=5, column=1, pady=15, padx=10)

CalculatedSgstLabel = Label(TotalMenuFrame, text='SGST (Rs)', font=('times new roman', 15, 'bold'))
CalculatedSgstLabel.grid(row=6, column=0, padx=10)
CalculatedSgstEntry = Entry(TotalMenuFrame, font=('arial', 15), width=10)
CalculatedSgstEntry.grid(row=6, column=1, pady=15, padx=10)


TotalPayableLabel = Label(TotalMenuFrame, text='Total Payable', font=('times new roman', 20, 'bold'))
TotalPayableLabel.grid(row=7, column=0, padx=10)
TotalPayableEntry = Label(TotalMenuFrame, font=('arial', 20, 'bold'), width=10, foreground='Green', relief='ridge')
TotalPayableEntry.grid(row=7, column=1, pady=15, padx=10)
TotalPayableEntry['text'] = '120'


################################################################################################################################
LastRowFrame = Frame(selling_window)
LastRowFrame.pack(fill=BOTH, padx=10)


#################################################################################################################################
PaymentMenuFrame = LabelFrame(LastRowFrame, text='Payment Section', font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
PaymentMenuFrame.grid(row=0, column=0, padx=10, sticky='e')

OnlineCheckVar = IntVar()
CashCheckVar = IntVar()
CreditCheckVar = IntVar()

OnlinePaymentButton = Checkbutton(PaymentMenuFrame, text = "Online", variable = OnlineCheckVar, command=payment_clciked, 
                             onvalue = 1, offvalue = 0, height = 1, width = 12, disabledforeground='white',
                             font=('arial', 16, 'bold'), border=5, )
OnlinePaymentButton.grid(row=0,column=0)

CashPaymentButton = Checkbutton(PaymentMenuFrame, text = "Cash", variable = CashCheckVar, command=payment_clciked,
                             onvalue = 1, offvalue = 0, height = 1, width = 12, disabledforeground='white', 
                             font=('arial', 16, 'bold'), border=5, )
CashPaymentButton.grid(row=0,column=1)

CreditPaymentButton = Checkbutton(PaymentMenuFrame, text = "Credit", variable = CreditCheckVar, command=payment_clciked,
                                  onvalue = 1, offvalue = 0, height = 1, width = 12, disabledforeground='white', 
                                  font=('arial', 16, 'bold'), border=5, )
CreditPaymentButton.grid(row=0,column=2)


#################################################################################################################################
BankDetailsframe = Frame(PaymentMenuFrame)
BankDetailsframe.grid(row=1, column=0, columnspan=3)

BankNameLabel = LabelFrame(BankDetailsframe, text="Bank Name")
BankNameLabel.grid(row=0, column=0, pady=5, padx=5)
BankNameEntry = Entry(BankNameLabel, state='disabled', font=('arial', 12))
BankNameEntry.grid(row=0, column=0, padx=5)

AccountNumberLabel = LabelFrame(BankDetailsframe, text="A/c No")
AccountNumberLabel.grid(row=0, column=1, padx=5)
AccountNumberEntry = Entry(AccountNumberLabel, state='disabled', width=25, font=('arial', 12))
AccountNumberEntry.grid(row=0, column=0, padx=5)

IfscCodeLabel = LabelFrame(BankDetailsframe, text='IFSC code')
IfscCodeLabel.grid(row=0, column=2, padx=5)
IfscCodeEntry = Entry(IfscCodeLabel, state='disabled', font=('arial', 12))
IfscCodeEntry.grid(row=0, column=0, padx=5)

DueDateLabel = LabelFrame(BankDetailsframe, text='Due date')
DueDateLabel.grid(row=0, column=3, padx=5)
DueDateEntry = Entry(DueDateLabel, state='disabled', font=('arial', 12))
DueDateEntry.grid(row=0, column=0, padx=5)

#################################################################################################################################
BillFrame = LabelFrame(LastRowFrame, text='Buttons Menu',font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE, pady=8)
BillFrame.grid(row=0, column=2,padx=10, sticky='w')

TotalButton = Button(BillFrame, text='Total', command=find_total, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
TotalButton.grid(row=0, column=0, padx=10, pady=10)

BillButton = Button(BillFrame, text='Bill', command=create_bill, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
BillButton.grid(row=0, column=1, padx=10, pady=10)

ClearButton = Button(BillFrame, text='Clear', command=clear_all_details, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
ClearButton.grid(row=0, column=2, padx=10, pady=10)

def exit_window():
    selling_window.destroy()
ExitButton = Button(BillFrame, text='Exit', command=exit_window, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
ExitButton.grid(row=0, column=3, padx=10, pady=10)



selling_window.mainloop()