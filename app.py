from tkinter import *
from tkinter import ttk, messagebox, font
from customtkinter import *
import datetime
from QR import generate_qr,decode_qr
import pandas as pd
from tkcalendar import Calendar
from doc_gen import generate_selling_bill
from num2words import num2words


set_appearance_mode("Light")

class sell_py():
    def __init__(self):
        self.selling_dictionary = {
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
        self.invoice_items = []
        self.total = 0
        self.selected = ''
        #################################################################################################################################
        set_appearance_mode("Light")

        self.selling_window = Toplevel()
        self.selling_window.geometry('1730x880+0+0')
        self.selling_window.title("Sales")
        # new_root.attributes('-topmost',True)

        #################################################################################################################################
        self.HeadingLabel = Label(self.selling_window, text='Selling Department', font=('URW Chancery L', 50, 'bold'), relief='raised', border=5)
        self.HeadingLabel.pack(fill=X, padx=10,pady=5)

        #################################################################################################################################
        self.customer_details_frame = LabelFrame(self.selling_window, text="Customer Details",font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
        self.customer_details_frame.pack(fill=X, padx=10)

        self.billNoLabel = Label(self.customer_details_frame, text='Bill No')
        self.billNoLabel.grid(row=0,column=0, padx=10, pady=10)

        self.billNoEntry = Entry(self.customer_details_frame)
        self.billNoEntry.grid(row=0, column=1, padx=15)

        self.NameLabel = Label(self.customer_details_frame, text='Name')
        self.NameLabel.grid(row=0, column=2, padx=10)

        self.NameEntry = Entry(self.customer_details_frame)
        self.NameEntry.grid(row=0,column=3, padx=15)

        self.NumberLabel = Label(self.customer_details_frame, text='Number',)
        self.NumberLabel.grid(row=0, column=4, padx=10)

        self.NumberEntry = Entry(self.customer_details_frame)
        self.NumberEntry.grid(row=0, column=5, padx=15)

        self.GstNumberLabel = Label(self.customer_details_frame, text='Customer Gst in : ')
        self.GstNumberLabel.grid(row=0, column=6, padx=10)

        self.GstNumberEntry = Entry(self.customer_details_frame)
        self.GstNumberEntry.grid(row=0, column=7, padx=15)

        self.TodayDateLabel = Label(self.customer_details_frame, text='Date')
        self.TodayDateLabel.grid(row=0, column=8, padx=10)

        self.TodayDateEntry = Entry(self.customer_details_frame)
        self.TodayDateEntry.grid(row=0, column=9)
        self.TodayDateEntry.insert(0,datetime.date.today().strftime("%d-%m-%Y"))

        refresh_image = PhotoImage(file='refresh.png')
        self.DateRefreshButton = Button(self.customer_details_frame, image=refresh_image, command=self.refresh_date)
        self.DateRefreshButton.grid(row=0, column=10, padx=5, pady=10)

        self.AddressLabel = Label(self.customer_details_frame, text='Address')
        self.AddressLabel.grid(row=1, column=0, padx=10)

        self.AddressEntry = Entry(self.customer_details_frame, width=90)
        self.AddressEntry.grid(row=1, column=1, pady=10, columnspan=5)

        #################################################################################################################################
        self.productFrame = LabelFrame(self.selling_window, text='Product Details',font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
        self.productFrame.pack(fill=X, padx=10)


        self.IdLabel = LabelFrame(self.productFrame, text='Id',font=('times new roman', 15, 'bold'),)
        self.IdLabel.grid(row=0, column=0, padx=4, pady=10)
        self.IdEntry = Entry(self.IdLabel, font=('arial', 15), width=3)
        self.IdEntry.grid(row=0, column=0, padx=10, pady=10)


        self.ItemQrLabel = LabelFrame(self.productFrame, text='QR Entry',font=('times new roman', 15, 'bold'))
        self.ItemQrLabel.grid(row=0, column=1, padx=4)
        self.ItemQrScan = Button(self.ItemQrLabel, text='Scan', width=7, command=self.QrScan)
        self.ItemQrScan.grid(row=0, column=0, pady=8, padx=5)


        self.ItemSerialNoLabel = LabelFrame(self.productFrame, text='Serial No',font=('times new roman', 15, 'bold'))
        self.ItemSerialNoLabel.grid(row=0, column=2, padx=4)
        self.ItemserialNoEntry = Entry(self.ItemSerialNoLabel, font=('arial', 15))
        self.ItemserialNoEntry.grid(row=0, column=0, pady=9, padx=5)


        self.ItemCategoryLabel = LabelFrame(self.productFrame, text='Item Category',font=('times new roman', 15, 'bold'))
        self.ItemCategoryLabel.grid(row=0, column=3, padx=4)
        self.items_list = ["Random","Low HP Pool", "Medium HP Pool", "High HP Pool", "Extreme HP Pool"]
        self.ItemCategoryEntry = StringVar() #initialize variable
        self.ItemCategoryComboBoxEntry = CTkComboBox(self.ItemCategoryLabel,
                                                        variable=self.ItemCategoryEntry, #set variable in combobox
                                                        values=self.items_list, width=200, font=('arial', 15))
        self.ItemCategoryComboBoxEntry.grid(row=0, column=0, pady=10, padx=10)


        self.ItemDescriptionLabel = LabelFrame(self.productFrame, text='Item Description',font=('times new roman', 15, 'bold'))
        self.ItemDescriptionLabel.grid(row=0, column=4, padx=4)
        self.ItemDescriptionEntry = Entry(self.ItemDescriptionLabel, font=('arial', 15), width=30)
        self.ItemDescriptionEntry.grid(row=0, column=0, pady=9, padx=10)


        self.ItemMrpLabel = LabelFrame(self.productFrame, text='MRP',font=('times new roman', 15, 'bold'))
        self.ItemMrpLabel.grid(row=0, column=5, padx=4)
        self.ItemMrpEntry = Entry(self.ItemMrpLabel, font=('arial', 15), width=10)
        self.ItemMrpEntry.grid(row=0, column=0, pady=9, padx=10)


        self.ItemDiscountLabel = LabelFrame(self.productFrame, text='Discount',font=('times new roman', 15, 'bold'))
        self.ItemDiscountLabel.grid(row=0, column=6, padx=4)
        self.ItemDiscountEntry = Entry(self.ItemDiscountLabel, font=('arial', 15), width=10)
        self.ItemDiscountEntry.grid(row=0, column=0, pady=9, padx=10)
        self.ItemDiscountEntry.insert(0,0)

        self.AddItemButton = Button(self.productFrame, text="➕ Add Item", command=self.add_item, border=3,)
        self.AddItemButton.grid(row=1, column=6)

        self.columns = ('id', 'serial_no', 'item_cat', 'item_desc', 'item_mrp', 'item_discount', 'item_total')
        self.selling_app_tree = ttk.Treeview(self.productFrame, columns=self.columns, show="headings", height=15)

        self.selling_app_tree.column('id', width=30, anchor=CENTER)
        self.selling_app_tree.column('serial_no', width=200, anchor=CENTER)
        self.selling_app_tree.column('item_cat', width=200, anchor=CENTER)
        self.selling_app_tree.column('item_desc', width=400, anchor=CENTER)
        self.selling_app_tree.column('item_mrp', width=150, anchor=E)
        self.selling_app_tree.column('item_discount', width=150, anchor=E)
        self.selling_app_tree.column('item_total', width=150, anchor=E)

        self.selling_app_tree.heading('id', text="ID")
        self.selling_app_tree.heading('serial_no', text="Serial Number")
        self.selling_app_tree.heading('item_cat', text="Category")
        self.selling_app_tree.heading('item_desc', text="Description")
        self.selling_app_tree.heading('item_mrp', text="MRP")
        self.selling_app_tree.heading('item_discount', text="Product Discount")
        self.selling_app_tree.heading('item_total', text="Total")

        self.selling_app_tree.grid(row=2, column=0, columnspan=7, padx=10, pady=10)

        self.style = ttk.Style(self.selling_app_tree)
        self.fnt=font.Font(size=12, family='arial')
        # self.style.configure('Treeview', rowheight=30)
        self.style.configure('Treeview', font=self.fnt)

        self.delete_record_button = Button(self.productFrame, text='Delete Record', command=self.delete_record)
        self.delete_record_button.grid(row=3, column=4, pady=10,sticky=E, padx=10)

        self.select_record_button = Button(self.productFrame, text="Select Record", command=self.select_record)
        self.select_record_button.grid(row=3, column=5,pady=10)

        self.update_record_button = Button(self.productFrame, text="Update Record", command=self.update_record)
        self.update_record_button.grid(row=3, column=6, pady=10)

        ##################################################################################################################################
        self.TotalMenuFrame = LabelFrame(self.productFrame, text="Total Menu",font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
        self.TotalMenuFrame.grid(row=0, column=7, rowspan=4)

        self.TotalAmtLabel = Label(self.TotalMenuFrame, text="Total Amt", font=('times new roman', 15, 'bold'))
        self.TotalAmtLabel.grid(row=0,column=0, pady=10, padx=10)
        self.TotalAmtEntry = Entry(self.TotalMenuFrame, font=('arial', 15), width=10)
        self.TotalAmtEntry.grid(row=0, column=1, pady=15, padx=10)

        self.DiscountLabel = Label(self.TotalMenuFrame, text="Extra Discount", font=('times new roman', 15, 'bold'))
        self.DiscountLabel.grid(row=1, column=0, pady=10, padx=10)
        self.DiscountEntry = Entry(self.TotalMenuFrame, font=('arial', 15), width=10)
        self.DiscountEntry.grid(row=1, column=1, pady=15, padx=10)
        self.DiscountEntry.insert(0, 0)

        self.CgstLabel = Label(self.TotalMenuFrame, text='CGST (%)', font=('times new roman', 15, 'bold'))
        self.CgstLabel.grid(row=2, column=0, padx=10)
        self.CgstEntry = Entry(self.TotalMenuFrame, font=('arial', 15), width=10)
        self.CgstEntry.grid(row=2, column=1, pady=15, padx=10)
        self.CgstEntry.insert(0,9)

        self.SgstLabel = Label(self.TotalMenuFrame, text='SGST (%)', font=('times new roman', 15, 'bold'))
        self.SgstLabel.grid(row=3, column=0, padx=10)
        self.SgstEntry = Entry(self.TotalMenuFrame, font=('arial', 15), width=10)
        self.SgstEntry.grid(row=3, column=1, pady=15, padx=10)
        self.SgstEntry.insert(0,9)

        self.TotalTaxableLabel = Label(self.TotalMenuFrame, text='Total taxable', font=('times new roman', 15, 'bold'))
        self.TotalTaxableLabel.grid(row=4, column=0, padx=10)
        self.TotalTaxableEntry = Entry(self.TotalMenuFrame, font=('arial', 15, 'bold'), width=10)
        self.TotalTaxableEntry.grid(row=4, column=1, pady=15, padx=10)

        self.CalculatedCgstLabel = Label(self.TotalMenuFrame, text='CGST (Rs)', font=('times new roman', 15, 'bold'))
        self.CalculatedCgstLabel.grid(row=5, column=0, padx=10)
        self.CalculatedCgstEntry = Entry(self.TotalMenuFrame, font=('arial', 15), width=10)
        self.CalculatedCgstEntry.grid(row=5, column=1, pady=15, padx=10)

        self.CalculatedSgstLabel = Label(self.TotalMenuFrame, text='SGST (Rs)', font=('times new roman', 15, 'bold'))
        self.CalculatedSgstLabel.grid(row=6, column=0, padx=10)
        self.CalculatedSgstEntry = Entry(self.TotalMenuFrame, font=('arial', 15), width=10)
        self.CalculatedSgstEntry.grid(row=6, column=1, pady=15, padx=10)

        self.TotalPayableLabel = Label(self.TotalMenuFrame, text='Total Payable', font=('times new roman', 20, 'bold'))
        self.TotalPayableLabel.grid(row=7, column=0, padx=10)
        self.TotalPayableEntry = Label(self.TotalMenuFrame, font=('arial', 20, 'bold'), width=10, foreground='Green', relief='ridge')
        self.TotalPayableEntry.grid(row=7, column=1, pady=15, padx=10)
        self.TotalPayableEntry['text'] = '0'

        ################################################################################################################################
        self.LastRowFrame = Frame(self.selling_window)
        self.LastRowFrame.pack(fill=BOTH, padx=10)


        #################################################################################################################################
        self.PaymentMenuFrame = LabelFrame(self.LastRowFrame, text='Payment Section', font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
        self.PaymentMenuFrame.grid(row=0, column=0, padx=10, sticky='e')

        self.OnlineCheckVar = IntVar()
        self.CashCheckVar = IntVar()
        self.CreditCheckVar = IntVar()

        OnlinePaymentButton = Checkbutton(self.PaymentMenuFrame, text = "Online", variable = self.OnlineCheckVar, command=self.payment_clciked, 
                                    onvalue = 1, offvalue = 0, height = 1, width = 12, disabledforeground='white',
                                    font=('arial', 16, 'bold'), border=5, )
        OnlinePaymentButton.grid(row=0,column=0)

        CashPaymentButton = Checkbutton(self.PaymentMenuFrame, text = "Cash", variable = self.CashCheckVar, command=self.payment_clciked,
                                    onvalue = 1, offvalue = 0, height = 1, width = 12, disabledforeground='white', 
                                    font=('arial', 16, 'bold'), border=5, )
        CashPaymentButton.grid(row=0,column=1)

        CreditPaymentButton = Checkbutton(self.PaymentMenuFrame, text = "Credit", variable = self.CreditCheckVar, command=self.payment_clciked,
                                        onvalue = 1, offvalue = 0, height = 1, width = 12, disabledforeground='white', 
                                        font=('arial', 16, 'bold'), border=5, )
        CreditPaymentButton.grid(row=0,column=2)


        #################################################################################################################################
        self.BankDetailsframe = Frame(self.PaymentMenuFrame)
        self.BankDetailsframe.grid(row=1, column=0, columnspan=3)

        self.BankNameLabel = LabelFrame(self.BankDetailsframe, text="Bank Name")
        self.BankNameLabel.grid(row=0, column=0, pady=5, padx=5)
        self.BankNameEntry = Entry(self.BankNameLabel, state='disabled', font=('arial', 12))
        self.BankNameEntry.grid(row=0, column=0, padx=5)

        self.AccountNumberLabel = LabelFrame(self.BankDetailsframe, text="A/c No")
        self.AccountNumberLabel.grid(row=0, column=1, padx=5)
        self.AccountNumberEntry = Entry(self.AccountNumberLabel, state='disabled', width=25, font=('arial', 12))
        self.AccountNumberEntry.grid(row=0, column=0, padx=5)

        self.IfscCodeLabel = LabelFrame(self.BankDetailsframe, text='IFSC code')
        self.IfscCodeLabel.grid(row=0, column=2, padx=5)
        self.IfscCodeEntry = Entry(self.IfscCodeLabel, state='disabled', font=('arial', 12))
        self.IfscCodeEntry.grid(row=0, column=0, padx=5)

        self.DueDateLabel = LabelFrame(self.BankDetailsframe, text='Due date')
        self.DueDateLabel.grid(row=0, column=3, padx=5)
        self.DueDateEntry = Entry(self.DueDateLabel, state='disabled', font=('arial', 12))
        self.DueDateEntry.grid(row=0, column=0, padx=5)

        #################################################################################################################################
        self.BillFrame = LabelFrame(self.LastRowFrame, text='Buttons Menu',font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE, pady=8)
        self.BillFrame.grid(row=0, column=2,padx=10, sticky='w')

        self.TotalButton = Button(self.BillFrame, text='Total', command=self.find_total, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
        self.TotalButton.grid(row=0, column=0, padx=10, pady=10)

        self.BillButton = Button(self.BillFrame, text='Bill', command=self.create_bill, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
        self.BillButton.grid(row=0, column=1, padx=10, pady=10)

        self.ClearButton = Button(self.BillFrame, text='Clear', command=self.clear_all_details, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
        self.ClearButton.grid(row=0, column=2, padx=10, pady=10)

        self.ExitButton = Button(self.BillFrame, text='Exit', command=self.exit_window, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
        self.ExitButton.grid(row=0, column=3, padx=10, pady=10)



        self.selling_window.mainloop()


    def add_to_database(self):
        try:
            self.sell_df = pd.read_csv('Sell.csv')
        except:
            self.sell_df = pd.DataFrame()
        self.buy_df = pd.read_csv('Buy.csv')
        if self.buy_df.shape == (0,0):
            messagebox.showinfo("Error", "0 Products in inventory.")
        self.indexes = []
        for item in self.invoice_items:
            self.temp_df = self.buy_df.loc[self.buy_df['Serial Number']==item[1]]
            if self.temp_df.size==0:
                messagebox.showerror("Not Found", f"SERIAL NO : {item[1]} \nnot found int he database \n\nDescription : {item[3]}")
                return False
            index = self.temp_df.index[0]
            self.indexes.append(index)
            self.selling_dictionary['Bill No'].append(self.billNoEntry.get())
            self.selling_dictionary['Seller Name'].append(self.temp_df['Seller Name'].values[0])
            self.selling_dictionary['Customer Name'].append(self.NameEntry.get())
            self.selling_dictionary['Buying Date'].append(self.temp_df['Buying Date'].values[0])
            self.selling_dictionary['Selling Date'].append(self.TodayDateEntry.get())
            self.selling_dictionary['Serial Number'].append(self.temp_df['Serial Number'].values[0])
            self.selling_dictionary['Product Category'].append(self.temp_df['Product Category'].values[0])
            self.selling_dictionary['Product Description'].append(self.temp_df['Product Description'].values[0])
            self.selling_dictionary['Buying Price'].append(self.temp_df['Buying Price'].values[0])
            self.selling_dictionary['Selling Price'].append(item[-1])
            self.selling_dictionary['Profit'].append(int(item[-1])-int(self.temp_df['Buying Price'].values[0]))
        self.temp_df = pd.DataFrame(self.selling_dictionary)
        self.sell_df = pd.concat([self.sell_df, self.temp_df])
        self.sell_df.to_csv('Sell.csv', index=False)
        self.buy_df.drop(index=self.indexes, inplace=True)
        self.buy_df.reset_index(inplace=True, drop=True)
        self.buy_df.to_csv('Buy.csv', index=False)
        return True

    def refresh_date(self):
        self.TodayDateEntry.delete(0, END)
        self.TodayDateEntry.insert(0,datetime.date.today().strftime("%d-%m-%Y"))

    def clear_product_area(self):
        self.IdEntry.delete(0,END)
        self.ItemserialNoEntry.delete(0,END)
        self.ItemCategoryEntry.set('')
        self.ItemDescriptionEntry.delete(0,END)
        self.ItemMrpEntry.delete(0,END)
        self.ItemDiscountEntry.delete(0,END)


    def clear_all_details(self):
        self.invoice_items = []
        self.NameEntry.delete(0,END)
        self.NumberEntry.delete(0,END)
        self.GstNumberEntry.delete(0,END)
        self.TodayDateEntry.delete(0,END)
        self.TodayDateEntry.insert(0,datetime.date.today().strftime("%d-%m-%Y"))
        self.billNoEntry.delete(0,END)
        self.AddressEntry.delete(0, END)
        self.selling_app_tree.delete(*self.selling_app_tree.get_children())
        self.TotalAmtEntry.delete(0,END)
        self.DiscountEntry.delete(0,END)
        self.DiscountEntry.insert(0,0)
        self.CgstEntry.delete(0,END)
        self.CgstEntry.insert(0,9)
        self.SgstEntry.delete(0,END)
        self.SgstEntry.insert(0,9)
        self.TotalTaxableEntry.delete(0,END)
        self.CalculatedCgstEntry.delete(0,END)
        self.CalculatedSgstEntry.delete(0,END)
        self.TotalPayableEntry['text'] = '0.00'
        self.BankNameEntry.delete(0,END)
        self.AccountNumberEntry.delete(0, END)
        self.IfscCodeEntry.delete(0, END)
        self.DueDateEntry.delete(0, END)
        self.clear_product_area()


    def add_item(self):
        if self.IdEntry.get() == '':
            messagebox.showerror("Error", "Please Enter ID")
        elif self.ItemserialNoEntry.get()=='':
            messagebox.showerror("Error", "Please Enter Serial No")
        elif self.ItemCategoryEntry.get()=='':
            messagebox.showerror("Error", "Please Select Category")
        elif self.ItemDescriptionEntry.get()=='':
            messagebox.showerror("Error", "Please Enter Product Description")
        elif self.ItemMrpEntry.get()=='':
            messagebox.showerror("Error", "Please Enter MRP")
        else:
            mrp = int(self.ItemMrpEntry.get())
            discount = int(self.ItemDiscountEntry.get())
            total = mrp-discount
            self.selling_app_tree.insert('', END, 
                        values=(
                            self.IdEntry.get(),
                            self.ItemserialNoEntry.get(),
                            self.ItemCategoryEntry.get(),
                            self.ItemDescriptionEntry.get(),
                            mrp,
                            discount, 
                            total) 
                            )
            self.clear_product_area()

    def select_record(self):
        self.selected = self.selling_app_tree.focus()
        if self.selected != '':
            self.values = self.selling_app_tree.item(self.selected, 'values')
            self.clear_product_area()
            self.IdEntry.insert(0,self.values[0])
            self.ItemserialNoEntry.insert(0, self.values[1])
            self.ItemCategoryEntry.set(self.values[2])
            self.ItemDescriptionEntry.insert(0,self.values[3])
            self.ItemMrpEntry.insert(0,self.values[4])
            self.ItemDiscountEntry.insert(0,self.values[5])
        else:
            messagebox.showerror("Error", "No Data row is selected!")

    def update_record(self):
        if self.selected !='':    
            self.selling_app_tree.item(self.selected, text="", values=(self.IdEntry.get(),self.ItemserialNoEntry.get(),self.ItemCategoryEntry.get(),self.ItemDescriptionEntry.get(),self.ItemMrpEntry.get(),self.ItemDiscountEntry.get(),int(self.ItemMrpEntry.get())-int(self.ItemDiscountEntry.get())))
            self.clear_product_area()
            self.selected = ''
        else:
            messagebox.showerror("Error", "Please Select record first \n then update it")


    def delete_record(self):
        try:
            selected_item = self.selling_app_tree.selection()[0] ## get selected item
            self.selling_app_tree.delete(selected_item)
        except:
            messagebox.showerror("Error", "No Record was selected")


    def QrScan(self):
        buy_df = pd.read_csv('Buy.csv')
        self.serial_no = decode_qr()
        self.temp_df = buy_df.loc[buy_df['Serial Number']==self.serial_no]
        if self.temp_df.size>0:
            self.ItemserialNoEntry.delete(0,END)
            self.ItemserialNoEntry.insert(0,self.serial_no)
            self.ItemCategoryEntry.set(self.temp_df.values[0][3])
            self.ItemDescriptionEntry.delete(0,END)
            self.ItemDescriptionEntry.insert(0,self.temp_df.values[0][4])
            self.ItemMrpEntry.delete(0,END)
            self.ItemMrpEntry.insert(0,self.temp_df.values[0][6])
            self.ItemDiscountEntry.delete(0,END)
            self.ItemDiscountEntry.insert(0,self.temp_df.values[0][7])
        else:
            messagebox.showwarning("Error","Product Not Found")
        return


    def all_product_sum(self):
        self.invoice_items = []
        self.temp_total = 0.0
        for child in self.selling_app_tree.get_children():
            self.invoice_items.append(self.selling_app_tree.item(child, 'values'))
            self.temp_total += float(self.selling_app_tree.item(child, 'values')[6])
        return self.temp_total


    def find_total(self):
        # Calculate Total form products
        self.total = self.all_product_sum()
        self.TotalAmtEntry.delete(0,END)
        self.TotalAmtEntry.insert(0, f"{self.total:.2f}")
        # Calculate Taxable amount
        self.new_total = self.total-int(self.DiscountEntry.get())
        self.TotalTaxableEntry.delete(0, END)
        self.TotalTaxableEntry.insert(0,f"{self.new_total:.2f}")
        # Calculate csgt and sgst
        self.calc_cgst = self.new_total*float(self.CgstEntry.get())/100
        self.calc_sgst = self.new_total*float(self.SgstEntry.get())/100
        self.CalculatedCgstEntry.delete(0,END)
        self.CalculatedCgstEntry.insert(0, self.calc_cgst)
        self.CalculatedSgstEntry.delete(0, END)
        self.CalculatedSgstEntry.insert(0, self.calc_sgst)
        # Calculate Grand Total Amount
        self.new_total += self.calc_cgst+ self.calc_sgst
        self.TotalPayableEntry['text'] = self.new_total


    def get_payment_mode(self):
        if self.CashCheckVar.get()==1:
            return "Cash"
        elif self.CreditCheckVar.get()==1:
            return "Credit"
        elif self.OnlineCheckVar.get()==1:
            return "Online"
        return

    def get_bank_details(self):
        if self.CreditCheckVar.get()==1:
            string = ''
            string += f"Bank : {self.BankNameEntry.get()}\n"
            string += f"A/c No : {self.AccountNumberEntry.get()}\n"
            string += f"IFSC : {self.IfscCodeEntry.get()}\n"
            string += f"Due : {self.DueDateEntry.get()}"
            return string
        else:
            return ''

    def create_bill(self):
        if self.NameEntry.get()=='':
            return messagebox.showerror("Error", "Please! Enter Customer Name. ")
        elif self.NumberEntry.get()=='':
            return messagebox.showerror("Error", "Please! Enter Customer Phone number. ")
        elif self.AddressEntry.get()=='':
            return messagebox.showerror("Error", "Please! Enter Customer address. ")
        elif self.TodayDateEntry.get()=='':
            return messagebox.showerror("Error", "Please! click once Refresh date button. ")
        elif self.TotalAmtEntry.get()=='':
            return messagebox.showerror("Error", "Please! Find the total First. ")
        elif [self.CreditCheckVar.get(),self.CashCheckVar.get(),self.OnlineCheckVar.get()] == [0,0,0]:
            messagebox.showerror('Error', "Please chose payment method")
        elif not self.add_to_database():
            return
        else:
            self.total_items = 0
            for child in self.selling_app_tree.get_children():
                self.total_items+=1
            detail_dict = {
            'name': self.NameEntry.get(),
            'address':self.AddressEntry.get(),
            'number':self.NumberEntry.get(),
            'gst_number':self.GstNumberEntry.get(),
            'bill_no':self.billNoEntry.get(),
            'today_date':self.TodayDateEntry.get(),
            'payment_mode':self.get_payment_mode(),
            'bank_details':self.get_bank_details(),
            'total':self.TotalAmtEntry.get(),
            'total_discount':self.DiscountEntry.get(),
            'taxable_amt':self.TotalTaxableEntry.get(),
            'cgst':self.CalculatedCgstEntry.get(),
            'sgst':self.CalculatedSgstEntry.get(),
            'cgst_per':self.CgstEntry.get(),
            'sgst_per':self.SgstEntry.get(),
            'round_off':int(float(self.TotalPayableEntry['text']))-float(self.TotalPayableEntry['text']),
            'grand_total':int(float(self.TotalPayableEntry['text'])),
            'amount_in_words':num2words(int(float(self.TotalPayableEntry['text']))),
            'total_items':self.total_items,
            }
            generate_selling_bill(invoice_list=self.invoice_items, detail_dict=detail_dict)
            
            self.clear_content = messagebox.askokcancel('Clear', "Do you want to clear all the content on the screen?")
            if self.clear_content:
                self.clear_all_details()
            else:
                if messagebox.askokcancel("Clear", "Do you want to clear the Product details on the screen?"):
                    self.clear_product_area()


    def payment_clciked(self):
        if [self.OnlineCheckVar.get(),self.CashCheckVar.get(),self.CreditCheckVar.get()] in [[1,1,1], [0,0,0]]:
            self.OnlinePaymentButton['state'] = 'normal'
            self.CashPaymentButton['state'] = 'normal'
            self.CreditPaymentButton['state'] = 'normal'
            self.BankNameEntry['state'] = 'disabled';self.AccountNumberEntry['state'] = 'disabled'
            self.IfscCodeEntry['state'] = 'disabled';self.DueDateEntry['state'] = 'disabled'
        elif self.OnlineCheckVar.get()==1:
            self.OnlinePaymentButton['state'] = 'normal'
            self.CashPaymentButton['state'] = 'disabled'
            self.CreditPaymentButton['state'] = 'disabled'
            self.BankNameEntry['state'] = 'disabled';self.AccountNumberEntry['state'] = 'disabled'
            self.IfscCodeEntry['state'] = 'disabled';self.DueDateEntry['state'] = 'disabled'
        elif self.CashCheckVar.get()==1:
            self.OnlinePaymentButton['state'] = 'disabled'
            self.CashPaymentButton['state'] = 'normal'
            self.CreditPaymentButton['state'] = 'disabled'
            self.BankNameEntry['state'] = 'disabled';self.AccountNumberEntry['state'] = 'disabled'
            self.IfscCodeEntry['state'] = 'disabled';self.DueDateEntry['state'] = 'disabled'
        elif self.CreditCheckVar.get()==1:
            self.OnlinePaymentButton['state'] = 'disabled'
            self.CashPaymentButton['state'] = 'disabled'
            self.CreditPaymentButton['state'] = 'normal'
            self.BankNameEntry['state'] = 'normal';self.AccountNumberEntry['state'] = 'normal'
            self.IfscCodeEntry['state'] = 'normal';self.DueDateEntry['state'] = 'normal'
            messagebox.showinfo("Process", "For Credit, Please Enter Bank details")

    def exit_window(self):
        # self.selling_window.eval('::ttk::CancelRepeat')
        self.selling_window.destroy()


class buy_py():
    pass
    def __init__(self) -> None:
        ################################################################################################################################
        set_appearance_mode("Light")

        self.buying_window = Toplevel()
        self.buying_window.geometry('2000x400')
        self.buying_window.title("Sales")

        #################################################################################################################################
        self.HeadingLabel = Label(self.buying_window, text='Buying Department', font=('URW Chancery L', 30, 'bold'))
        self.HeadingLabel.pack(fill=X)

        self.customer_details_frame = LabelFrame(self.buying_window, text="Customer Details",font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
        self.customer_details_frame.pack(fill=X)

        self.TodayDateLabel = Label(self.customer_details_frame, text='Date')
        self.TodayDateLabel.grid(row=0, column=0, padx=10)

        self.TodayDateEntry = Entry(self.customer_details_frame)
        self.TodayDateEntry.grid(row=0, column=1, padx=15, pady=10)
        self.TodayDateEntry.insert(0,datetime.date.today().strftime("%d-%m-%Y"))

        #################################################################################################################################
        self.productFrame = LabelFrame(self.buying_window, text='Product Details',font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
        self.productFrame.pack(fill=X)

        self.IdLabel = LabelFrame(self.productFrame, text='Id',font=('times new roman', 15, 'bold'),)
        self.IdLabel.grid(row=0, column=0, padx=4, pady=10)
        self.itemIdEntry = Label(self.IdLabel, text='1', font=('arial', 15, 'bold'))
        self.itemIdEntry.grid(row=0, column=0, padx=10, pady=10)

        self.ItemClientLabel = LabelFrame(self.productFrame, text='Client Name',font=('times new roman', 15, 'bold'))
        self.ItemClientLabel.grid(row=0, column=1, padx=4)
        self.ClientName = Entry(self.ItemClientLabel, width=20, font=('arial', 15))
        self.ClientName.grid(row=0, column=0, pady=8, padx=5)

        self.SerialNoLabel = LabelFrame(self.productFrame, text='Serial No',font=('times new roman', 15, 'bold'))
        self.SerialNoLabel.grid(row=0, column=2, padx=4)
        self.serialNoEntry = Entry(self.SerialNoLabel, font=('arial', 15))
        self.serialNoEntry.grid(row=0, column=0, pady=9, padx=5)

        self.ItemCategoryLabel = LabelFrame(self.productFrame, text='Item Category',font=('times new roman', 15, 'bold'))
        self.ItemCategoryLabel.grid(row=0, column=3, padx=4)
        self.items_list = ["Refrigerator", 'Air Conditioner', 'Atta chakki', 'Fan', 'Washing Machine', 'Television', 'Purifier']
        self.itemCategoryEntry = StringVar() 
        self.CategoryList = CTkComboBox(self.ItemCategoryLabel, variable=self.itemCategoryEntry, values=self.items_list, width=200, font=('arial', 18))
        self.CategoryList.grid(row=0, column=0, pady=10, padx=10)

        self.ItemDescriptionLabel = LabelFrame(self.productFrame, text='Item Description',font=('times new roman', 15, 'bold'))
        self.ItemDescriptionLabel.grid(row=0, column=4, padx=4)
        self.itemDescriptionEntry = Entry(self.ItemDescriptionLabel, width=50, font=('arial', 15))
        self.itemDescriptionEntry.grid(row=0, column=0, pady=9, padx=10)

        self.ItemBuyingLabel = LabelFrame(self.productFrame, text='Buying (Rs.)',font=('times new roman', 15, 'bold'))
        self.ItemBuyingLabel.grid(row=0, column=5, padx=4)
        self.ItemBuyingEntry = Entry(self.ItemBuyingLabel, font=('arial', 15), width=10)
        self.ItemBuyingEntry.grid(row=0, column=0, pady=9, padx=10)

        self.ItemMrpLabel = LabelFrame(self.productFrame, text='MRP',font=('times new roman', 15, 'bold'))
        self.ItemMrpLabel.grid(row=0, column=6, padx=4)
        self.MrpEntry = Entry(self.ItemMrpLabel, font=('arial', 15), width=10)
        self.MrpEntry.grid(row=0, column=0, pady=9, padx=10)

        self.ItemDiscountLabel = LabelFrame(self.productFrame, text='Discount',font=('times new roman', 15, 'bold'))
        self.ItemDiscountLabel.grid(row=0, column=7, padx=4)
        self.DiscountEntry = Entry(self.ItemDiscountLabel, font=('arial', 15), width=10)
        self.DiscountEntry.grid(row=0, column=0, pady=9, padx=10)
        self.DiscountEntry.insert(0,0)



        #################################################################################################################################
        self.BillFrame = LabelFrame(self.buying_window, text='Bill Menu',font=('DejaVu Math TeX Gyre', 20, 'underline'),border=8, relief=GROOVE)
        self.BillFrame.pack()

        self.AddButton = Button(self.BillFrame, text='Add to Inventory', command=self.save_to_inventory, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
        self.AddButton.grid(row=0, column=0, padx=10, pady=10)

        self.QrButton = Button(self.BillFrame, text='Generate Qr', command=self.print_qr, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
        self.QrButton.grid(row=0, column=1, padx=10, pady=10)

        self.ClearButton = Button(self.BillFrame, text='Clear', command=self.clear_buying_window, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
        self.ClearButton.grid(row=0, column=2, padx=10, pady=10)

        self.ExitButton = Button(self.BillFrame, text='Exit', command=self.exit_window, font=('Andale Mono',15, 'bold'), pady=10, padx=10, border=5)
        self.ExitButton.grid(row=0, column=3, padx=10, pady=10)
        self.buying_window.mainloop()




    def reinitiate_dict(self):
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


    def save_to_inventory(self):
        if self.itemCategoryEntry.get() not in self.items_list:
            messagebox.showerror("Error","Select correct Product Category")
        elif self.itemDescriptionEntry.get()=='':
            messagebox.showerror("Error", "Please Give Product Description")
        elif self.ItemBuyingEntry.get() == "":
            messagebox.showerror("Error", "Please Enter Buying Price")
        elif self.MrpEntry.get()=='':
            messagebox.showerror("Error", "Please Enter MRP")
        elif self.serialNoEntry.get() == '':
            messagebox.showerror("Error","Please Enter Serial Number")
        elif self.ClientName.get() == "":
            messagebox.showerror("Error", "Please Enter Client name")
        else:
            self.reinitiate_dict()
            try:
                df = pd.read_csv('Buy.csv')
            except:
                df = pd.DataFrame(data_dict)
            data_dict["Seller Name"].append(self.ClientName.get())
            data_dict["Serial Number"].append(self.serialNoEntry.get())
            data_dict["Product Category"].append(self.itemCategoryEntry.get())
            data_dict["Product Description"].append(self.itemDescriptionEntry.get())
            data_dict["Buying Price"].append(self.ItemBuyingEntry.get())
            data_dict["Buying Date"].append(self.TodayDateEntry.get())
            data_dict["MRP"].append(self.MrpEntry.get())
            data_dict["Discount"].append(self.DiscountEntry.get())
            df = pd.concat([df,pd.DataFrame(data_dict)])
            df.to_csv('Buy.csv', index=None)
            messagebox.showinfo("Done", "Successfully Added to the inventory.")


    def print_qr(self):
        text = self.serialNoEntry.get()
        # + '\n'
        # text += itemCategoryEntry.get() + '\n'
        # text += itemDescriptionEntry.get() + '\n'
        # text += MrpEntry.get() + '\n'
        # text += DiscountEntry.get() + '\n'
        if generate_qr(text):
            messagebox.showinfo("Success", "QR Generated successfully!")
        else:
            messagebox.showinfo("Error", "No QR generated!")
            


    def clear_buying_window(self):
        self.serialNoEntry.delete(0, END)
        self.ClientName.delete(0,END)
        self.itemCategoryEntry.set('')
        self.itemDescriptionEntry.delete(0, END)
        self.ItemBuyingEntry.delete(0,END)
        self.MrpEntry.delete(0,END)
        self.DiscountEntry.delete(0,END)
        self.DiscountEntry.insert(0,0)

    def exit_window(self):
        self.buying_window.destroy()


class inventory_py():
    def __init__(self):
        set_appearance_mode("Light")
        self.selected = ''
        self.inventory_window = Toplevel()
        self.inventory_window.title("Stock Inventory ")
        self.inventory_window.geometry("1400x960")
        self.inventory_window.configure(bg='lightyellow1')

        self.df = pd.read_csv("Buy.csv")

        self.headingLabel = Label(self.inventory_window, text='Inventory', font=('URW Chancery L', 40, 'bold'), background='indigo', pady=5, foreground='white')
        self.headingLabel.pack(fill=X)

        self.inventory_tree = ttk.Treeview(self.inventory_window, show="headings", height=30)
        self.inventory_tree.pack(pady=10)
        self.inventory_tree["column"] = list(self.df.columns)
        self.inventory_tree["show"] = "headings"

        for col in self.inventory_tree["column"]:
            self.inventory_tree.heading(
                col, text=col, command=lambda c=col: self.sort_treeview(self.inventory_tree, c, False))
            if col == 'Product Description':
                self.inventory_tree.column(col, width=300)
            elif col in ['Buying Price', 'MRP', 'Discount']:
                self.inventory_tree.column(col, width=100, anchor=E)
            elif col in ['Serial Number', 'Seller Name', 'Buying Date']:
                self.inventory_tree.column(col, width=150, anchor=W)
            else:
                self.inventory_tree.column(col, width=200, anchor=CENTER)

        for item in self.df.values:
            items = list(i for i in item)
            self.inventory_tree.insert('', 'end', values=items)


        self.buttonsFrame1 = Frame(self.inventory_window, background='lightyellow1')
        self.buttonsFrame1.pack()

        self.selectButton = Button(self.buttonsFrame1, text="Select",command=self.select_record, background='gray80', activebackground='gray60', font=('times new roman', 15))
        self.selectButton.grid(row=0, column=0,padx=10)
        self.clearButton = Button(self.buttonsFrame1, text="Delete", command=self.delete_record, background='gray80', activebackground='gray60', font=('times new roman', 15))
        self.clearButton.grid(row=0, column=1)
        self.getQRButton = Button(self.buttonsFrame1, text="Get QR", command=self.get_qr, background='gray80', activebackground='gray60', font=('times new roman', 15))
        self.getQRButton.grid(row=0, column=2, padx=10)
        self.getQRButton = Button(self.buttonsFrame1, text="Refresh data", command=self.refresh_record, background='gray80', activebackground='gray60', font=('times new roman', 15))
        self.getQRButton.grid(row=0, column=3)


        self.entryFrame = Frame(self.inventory_window, border=5, relief='groove', background='lightyellow1')
        self.entryFrame.pack(pady=10, anchor=CENTER)

        self.SellerNameLabel = Label(self.entryFrame, text="Seller Name", font=('times new roman', 15), background='lightyellow1')
        self.SellerNameLabel.grid(row=0, column=0)
        self.SellerNameEntry = Entry(self.entryFrame, font=('arial', 13))
        self.SellerNameEntry.grid(row=1, column=0)


        self.SerialNumberLabel = Label(self.entryFrame, text="Serial No.", font=('times new roman', 15), background='lightyellow1')
        self.SerialNumberLabel.grid(row=0, column=1)
        self.SerialNumberEntry = Entry(self.entryFrame, font=('arial', 13))
        self.SerialNumberEntry.grid(row=1, column=1)


        self.BuyingDateLabel = Label(self.entryFrame, text="Buying Date", font=('times new roman', 15), background='lightyellow1')
        self.BuyingDateLabel.grid(row=0, column=2)
        self.BuyingDateEntry = Entry(self.entryFrame, font=('arial', 13))
        self.BuyingDateEntry.grid(row=1, column=2)


        self.itemCategoryLabel = Label(self.entryFrame, text="Category", font=('times new roman', 15), background='lightyellow1')
        self.itemCategoryLabel.grid(row=0, column=3)


        items_list = ["Random", "Low HP Pool",
                    "Medium HP Pool", "High HP Pool", "Extreme HP Pool"]
        self.ItemCategoryEntry = StringVar()
        self.ItemCategoryComboBoxEntry = CTkComboBox(self.entryFrame,
                                                            variable=self.ItemCategoryEntry,  # set variable in combobox
                                                            values=items_list, width=200, font=('arial', 15))
        self.ItemCategoryComboBoxEntry.grid(row=1, column=3, padx=10)


        self.ItemDescriptionLabel = Label(self.entryFrame, text="Description", font=('times new roman', 15), background='lightyellow1')
        self.ItemDescriptionLabel.grid(row=0, column=4)
        self.ItemDescriptionEntry = Entry(self.entryFrame, width=40, font=('arial', 13))
        self.ItemDescriptionEntry.grid(row=1, column=4, padx=10)


        self.ItemBuyingLabel = Label(self.entryFrame, text="Buying Price", font=('times new roman', 15), background='lightyellow1')
        self.ItemBuyingLabel.grid(row=2, column=0)
        self.ItemBuyingEntry = Entry(self.entryFrame, font=('arial', 13))
        self.ItemBuyingEntry.grid(row=3, column=0, padx=10)


        self.ItemMrpLabel = Label(self.entryFrame, text="MRP", font=('times new roman', 15), background='lightyellow1')
        self.ItemMrpLabel.grid(row=2, column=1, padx=10)
        self.ItemMrpEntry = Entry(self.entryFrame, font=('arial', 13))
        self.ItemMrpEntry.grid(row=3, column=1, padx=10)


        self.ItemDiscountLabel = Label(self.entryFrame, text="Discount", font=('times new roman', 15), background='lightyellow1')
        self.ItemDiscountLabel.grid(row=2, column=2, padx=10)
        self.ItemDiscountEntry = Entry(self.entryFrame, font=('arial', 13))
        self.ItemDiscountEntry.grid(row=3, column=2, padx=10, pady=5)


        self.buttonsFrame = Frame(self.inventory_window, background='lightyellow1')
        self.buttonsFrame.pack()


        self.searchButton = Button(self.buttonsFrame, text="Search", command=self.search_record, font=('times new roman',18), foreground='black', relief='raised', border=3, background='gray80', activebackground='gray60')
        self.searchButton.grid(row=0, column=1, padx=10)
        # updateButton = Button(self.buttonsFrame, text="Update", command=update_record, font=('times new roman',18), foreground='black', relief='raised', border=3, background='gray80', activebackground='gray60')
        # updateButton.grid(row=0, column=2, padx=10)
        self.clearButton = Button(self.buttonsFrame, text="Clear", command=self.clear_product_area, font=('times new roman',18), foreground='black', relief='raised', border=3, background='gray80', activebackground='gray60')
        self.clearButton.grid(row=0, column=3, padx=10)
        self.exitButton = Button(self.buttonsFrame, text="Exit", command=self.exit_window, font=('times new roman',18),foreground='black', relief='raised', border=3, background='gray80', activebackground='gray60')
        self.exitButton.grid(row=0, column=4, padx=10)

        self.inventory_window.mainloop()
    
    def exit_window(self):
        self.inventory_window. destroy()

    
    def clear_product_area(self):
        self.SerialNumberEntry.delete(0,END)
        self.SellerNameEntry.delete(0,END)
        self.BuyingDateEntry.delete(0,END)
        self.ItemCategoryEntry.set('')
        self.ItemDescriptionEntry.delete(0,END)
        self.ItemBuyingEntry.delete(0,END)
        self.ItemMrpEntry.delete(0,END)
        self.ItemDiscountEntry.delete(0,END)


    def select_record(self):
        self.selected = self.inventory_tree.focus()
        if self.selected != '':
            values = self.inventory_tree.item(self.selected, 'values')
            self.clear_product_area()
            self.SellerNameEntry.insert(0, values[0])
            self.SerialNumberEntry.insert(0, values[1])
            self.BuyingDateEntry.insert(0, values[2])
            self.ItemCategoryEntry.set(values[3])
            self.ItemDescriptionEntry.insert(0, values[4])
            self.ItemBuyingEntry.insert(0, values[5])
            self.ItemMrpEntry.insert(0, values[6])
            self.ItemDiscountEntry.insert(0, values[7])
        else:
            messagebox.showerror("Error", "No Data row is selected!")    


    def delete_record(self):
        self.selected = self.inventory_tree.focus()
        if self.selected != '':
            if not messagebox.askokcancel("", 'Do you really want to delete?'):
                return
            values = self.inventory_tree.item(self.selected, 'values')
            try:
                self.df = pd.read_csv('Buy.csv')
                self.df.drop(index=self.df[self.df['Serial Number']==values[1]].index, inplace=True)
                selected_item = self.inventory_tree.selection()[0]
                self.inventory_tree.delete(selected_item)
                self.df.to_csv('Buy.csv', index=False)
            except:
                messagebox.showerror("Error", "Found Error in the code.....")
                return
            messagebox.showinfo("Done", "Record Deleted from Inventory Sucessfully!")
        else:
            messagebox.showerror("Error", "No Data row is selected!")

    def get_qr(self):
        self.selected = self.inventory_tree.focus()
        if self.selected != '':
            values = self.inventory_tree.item(self.selected, 'values')
            if generate_qr(values[1]):
                messagebox.showinfo("Successfull", "Generated Qr Sucessfully")
            else:
                messagebox.showerror("Error", "Found Error in the code.....")
        else:
            messagebox.showerror("Error", "No Data row is selected!")

    def search_record(self):
        self.df = pd.read_csv('Buy.csv')
        new_df = pd.DataFrame()
        if self.SellerNameEntry.get()=='' and self.SerialNumberEntry.get()=='' and self.BuyingDateEntry.get()=='' and self.ItemCategoryEntry.get()=='' and self.ItemDescriptionEntry.get()=='' and self.ItemBuyingEntry.get()=='' and self.ItemMrpEntry.get()=='':
            messagebox.showerror('Error', "Please Enter any value to search!")
            return
        if self.SellerNameEntry.get()!='':
            seller_name = self.SellerNameEntry.get()
            new_df = self.df[self.df['Seller Name'].str.contains(seller_name, case=False)]
            
        if self.SerialNumberEntry.get()!='':
            serial_no = self.SerialNumberEntry.get()
            if len(new_df)>0:
                new_df = new_df[new_df['Serial Number'].str.contains(serial_no, case=False)]
            else:
                new_df = self.df[self.df['Serial Number'].str.contains(serial_no, case=False)]
                
        if self.BuyingDateEntry.get()!='':
            buying_date = self.BuyingDateEntry.get()
            if len(new_df)>0:
                new_df = new_df[new_df['Buying Date'].str.contains(buying_date, case=False)]
            else:
                new_df = self.df[self.df['Buying Date'].str.contains(buying_date, case=False)]
                
        if self.ItemCategoryEntry.get()!='':
            category = self.ItemCategoryEntry.get()
            if len(new_df)>0:
                new_df = new_df[new_df['Product Category'].str.contains(category, case=False)]
            else:
                new_df = self.df[self.df['Product Category'].str.contains(category, case=False)]
                
        if self.ItemDescriptionEntry.get()!='':
            description = self.ItemDescriptionEntry.get()
            if len(new_df)>0:
                new_df = new_df[new_df['Product Description'].str.contains(description, case=False)]
            else:
                new_df = self.df[self.df['Product Description'].str.contains(description, case=False)]
                
        if self.ItemBuyingEntry.get()!='':
            buying_price = int(self.ItemBuyingEntry.get())
            if len(new_df)>0:
                new_df = new_df[[True if (i==buying_price) else False for i in new_df['Buying Price']]]
            else:
                new_df = self.df[[True if (i==buying_price) else False for i in self.df['Buying Price']]]
                
        if self.ItemMrpEntry.get()!='':
            mrp = int(self.ItemMrpEntry.get())
            if len(new_df)>0:
                new_df = new_df[[True if (i==mrp) else False for i in new_df['MRP']]]
            else:
                new_df = self.df[[True if (i==mrp) else False for i in self.df['MRP']]]
        self.inventory_tree.delete(*self.inventory_tree.get_children())
        for item in new_df.values:
            items = list(i for i in item)
            self.inventory_tree.insert('', 'end', values=items)
        del new_df
        
    def refresh_record(self):
        self.inventory_tree.delete(*self.inventory_tree.get_children())
        for item in self.df.values:
            items = list(i for i in item)
            self.inventory_tree.insert('', 'end', values=items)

    def sort_treeview(self, inventory_tree, col, descending):
        data = [(inventory_tree.set(item, col), item) for item in inventory_tree.get_children('')]
        data.sort(reverse=descending)
        for index, (val, item) in enumerate(data):
            inventory_tree.move(item, '', index)
        inventory_tree.heading(col, command=lambda: self.sort_treeview(inventory_tree, col, not descending))


class sold_py():
    def __init__(self):
        self.sold_products_window = Toplevel()
        self.sold_products_window.title("Billed Products")
        self.sold_products_window.configure(bg='lightyellow1')

        self.df = pd.read_csv("Sell.csv")

        headingLabel = Label(self.sold_products_window, text='Sold Products History', font=('URW Chancery L', 40, 'bold'), background='indigo', pady=5, foreground='white')
        headingLabel.pack(fill=X)

        self.sold_products_tree = ttk.Treeview(self.sold_products_window, show="headings", height=20)
        self.sold_products_tree["column"] = list(self.df.columns)
        self.sold_products_tree["show"] = "headings"


        for col in self.sold_products_tree["column"]:
            self.sold_products_tree.heading(
                col, text=col, command=lambda c=col: self.sort_treeview(self.sold_products_tree, c, False))
            if col == 'Product Description':
                self.sold_products_tree.column(col, width=300)
            elif col == 'Bill No':
                self.sold_products_tree.column(col, width=100)
            elif col in ['Buying Price', 'MRP', 'Discount']:
                self.sold_products_tree.column(col, width=100, anchor=E)
            elif col in ['Serial Number', 'Seller Name',]:
                self.sold_products_tree.column(col, width=150, anchor=W)
            else:
                self.sold_products_tree.column(col, width=150, anchor=CENTER)

        for item in self.df.values:
            items = list(i for i in item)
            self.sold_products_tree.insert('', 'end', values=items)



        self.sold_products_tree.pack(pady=10)


        self.ListingFrame = LabelFrame(self.sold_products_window)
        self.ListingFrame.pack()

        self.ListingFrame1 = Frame(self.ListingFrame)
        self.ListingFrame1.grid(row=0, column=0, padx=50, rowspan=2)


        self.billNoLabel = CTkLabel(self.ListingFrame1, text='Bill No',width=100, text_color='black',font=('times new roman', 18, 'bold'))
        self.billNoLabel.grid(row=0, column=0)
        self.billNoEntry = CTkEntry(self.ListingFrame1, width=150, text_color='black', font=('arial', 18))
        self.billNoEntry.grid(row=0, column=1, pady=20)

        self.serialNumberLabel = CTkLabel(self.ListingFrame1,text='Serial No.',font=('times new roman', 18, 'bold'))
        self.serialNumberLabel.grid(row=1, column=0)
        self.serialNumberEntry = CTkEntry(self.ListingFrame1, width=150, text_color='black', font=('arial', 18))
        self.serialNumberEntry.grid(row=1, column=1, pady=20)


        self.sellingDateLabel = CTkLabel(self.ListingFrame1, text='Selling Date',font=('times new roman', 18, 'bold'))
        self.sellingDateLabel.grid(row=0, column=2, padx=20)
        self.sellingDateEntry = CTkEntry(self.ListingFrame1, width=150, text_color='black', font=('arial', 18))
        self.sellingDateEntry.grid(row=0, column=3)

        self.CategoryLabel = CTkLabel(self.ListingFrame1, text='Category',font=('times new roman', 18, 'bold'))
        self.CategoryLabel.grid(row=1, column=2)
        self.items_list = ["Refrigerator", 'Air Conditioner', 'Atta chakki', 'Fan', 'Washing Machine', 'Television', 'Purifier']
        self.itemCategoryEntry = StringVar() 
        self.CategoryEntry = CTkComboBox(self.ListingFrame1, variable=self.itemCategoryEntry, values=self.items_list, width=150, font=('arial', 18))
        self.CategoryEntry.grid(row=1, column=3, padx=10)

        self.ListingFrame2 = Frame(self.ListingFrame)
        self.ListingFrame2.grid(row=0, column=1, columnspan=2)

        self.add_date_range = StringVar(value="off")
        self.checkbox = CTkCheckBox(self.ListingFrame2, text="Add Dates Range", command=self.dates_check_box,
                                            variable=self.add_date_range, onvalue="on", offvalue="off", font=('times new roman', 25,), checkmark_color='chartreuse4',fg_color='white', hover_color='',)
        self.checkbox.grid(row=0, column=0, columnspan=2, pady=10)


        self.ListingFrame3 = Frame(self.ListingFrame)
        self.ListingFrame3.grid(row=1, column=1)

        self.FromDateLabel = CTkLabel(self.ListingFrame3, text='From : ',font=('times new roman', 18, 'bold'))
        self.FromDateLabel.grid(row=0, column=0)
        self.FromDate = Calendar(self.ListingFrame3, selectmode = 'day',
                    year = datetime.date.today().year, 
                    month = datetime.date.today().month,
                    day = datetime.date.today().day,)
        self.FromDate.grid(row=0, column=1)



        self.ListingFrame4 = Frame(self.ListingFrame)
        self.ListingFrame4.grid(row=1, column=2,padx=50)

        self.EndDateLabel = CTkLabel(self.ListingFrame4, text='To : ',font=('times new roman', 18, 'bold'))
        self.EndDateLabel.grid(row=0, column=0)
        self.EndDate = Calendar(self.ListingFrame4, selectmode = 'day',
                    year = datetime.date.today().year, 
                    month = datetime.date.today().month,
                    day = datetime.date.today().day,)
        self.EndDate.grid(row=0, column=1)

        self.EndDate['state']='disabled'
        self.FromDate['state'] = 'disabled'



        self.thirdFrame = Frame(self.sold_products_window, background='lightyellow1')
        self.thirdFrame.pack()

        self.BtnFrame = Frame(self.thirdFrame, background='lightyellow1')
        self.BtnFrame.grid(row=0, column=0, pady=10)

        self.SearchButton = Button(self.BtnFrame, text='Search', font=('times new roman', 18, 'bold'), border=3, command=self.search_record)
        self.SearchButton.grid(row=0, column=0, padx=20)
        self.ExitButton = Button(self.BtnFrame, text='Exit', font=('times new roman', 18, 'bold'), border=3, command=self.exit_window)
        self.ExitButton.grid(row=0, column=1, padx=20)
        self.RefreshButton = Button(self.BtnFrame, text='Refresh', font=('times new roman', 18, 'bold'), border=3, command=self.refresh_record)
        self.RefreshButton.grid(row=0, column=2, padx=20)

        self.ProfitFrame = LabelFrame(self.thirdFrame, background='lightyellow1', width=50, border=3)
        self.ProfitFrame.grid(row=0, column=1, padx=50, pady=10)

        self.ProfitLabel = Label(self.ProfitFrame, text='Total Profit', font=('times new roman', 18, 'bold'), background='lightyellow1', )
        self.ProfitLabel.grid(row=0, column=0,)

        self.ProfitEntryLabel = Label(self.ProfitFrame, text='0', font=('arial', 18, 'bold'),border=3, padx=5, pady=5, relief='ridge', width=10)
        self.ProfitEntryLabel.grid(row=0, column=1, padx=20, pady=10)


        self.find_profit()

        self.sold_products_window.mainloop()
        
    
    def sort_treeview(self, tree, col, descending):
        data = [(tree.set(item, col), item) for item in tree.get_children('')]
        data.sort(reverse=descending)
        for index, (val, item) in enumerate(data):
            tree.move(item, '', index)
        tree.heading(col, command=lambda: self.sort_treeview(tree, col, not descending))


    def dates_check_box(self):
        if self.add_date_range.get() == 'on':
            self.FromDate['state'] = 'normal'
            self.EndDate['state'] = 'normal'
        else:
            self.FromDate['state'] = 'disabled'
            self.EndDate['state'] = 'disabled'

    def find_profit(self):
        profit = 0
        for child in self.sold_products_tree.get_children(''):
            profit+=int(self.sold_products_tree.item(child, 'values')[-1])
        self.ProfitEntryLabel['text'] = profit
        self.clear_entry_zone()

    def search_record(self):
        if self.add_date_range.get() == 'on':
            new_df = self.df.loc[(pd.to_datetime(self.df['Selling Date'], dayfirst=True)>=pd.to_datetime(self.FromDate.get_date(), dayfirst=True))
                            &
                            (pd.to_datetime(self.df['Selling Date'], dayfirst=True)<=pd.to_datetime(self.EndDate.get_date(), dayfirst=True))]
            if len(new_df)==0:
                messagebox.showerror('Error', f'No Items sold in between {self.FromDate.get_date()} and {self.EndDate.get_date()}')
                del new_df
                self.clear_entry_zone()
                return
                    
        if self.sellingDateEntry.get()!='':
            string = self.sellingDateEntry.get()
            try:
                pd.to_datetime(string, dayfirst=True)
            except:
                messagebox.showerror("Error", "Wrong Date Entered.\nPlease check the date once again.")
                self.clear_entry_zone()
                return
            try :
                new_df = new_df.loc[pd.to_datetime(new_df['Selling Date'], dayfirst=True) == pd.to_datetime(string, dayfirst=True)]
            except:
                new_df = self.df.loc[pd.to_datetime(self.df['Selling Date'], dayfirst=True) == pd.to_datetime(string, dayfirst=True)]
            if len(new_df)==0:
                messagebox.showerror('Error', f'No Items sold for date : {string}')
                del new_df
                self.clear_entry_zone()
                return
        
        if self.billNoEntry.get()!='':
            billNo = self.billNoEntry.get()
            try:
                new_df = new_df.loc[new_df['Bill No']==billNo]
            except:
                new_df = self.df.loc[self.df['Bill No']==billNo]
            if len(new_df)==0:
                messagebox.showerror('Error', f'No Items sold with bill No : {billNo}')
                del new_df
                self.clear_entry_zone()
                return
        
        if self.CategoryEntry.get()!='':
            category = self.CategoryEntry.get()
            try:
                new_df = new_df.loc[new_df['Product Category'] == category]
            except:
                new_df = self.df.loc[self.df['Product Category'] == category]
            if len(new_df)==0:
                messagebox.showerror('Error', f'No Items sold with category : {category}')
                del new_df
                self.clear_entry_zone()
                return
            
        if self.serialNumberEntry.get()!='':
            serialNo = self.serialNumberEntry.get()
            try:
                new_df = new_df.loc[new_df['Serial Number'] == serialNo]
            except:
                new_df = self.df.loc[self.df['Serial Number'] == serialNo]
            if len(new_df)==0:
                messagebox.showerror('Error', f'No Items sold with Serial Number : {serialNo}')
                del new_df
                self.clear_entry_zone()
                return
        self.sold_products_tree.delete(*self.sold_products_tree.get_children())
        for item in new_df.values:
            items = list(i for i in item)
            self.sold_products_tree.insert('', 'end', values=items)
        self.find_profit()
        del new_df
        
    def clear_entry_zone(self):
        self.serialNumberEntry.delete(0,END)
        self.sellingDateEntry.delete(0,END)
        self.billNoEntry.delete(0,END)
        self.CategoryEntry.set('')
        
    def refresh_record(self):
        self.sold_products_tree.delete(*self.sold_products_tree.get_children())
        for item in self.df.values:
            items = list(i for i in item)
            self.sold_products_tree.insert('', 'end', values=items)
        self.clear_entry_zone()
        self.find_profit()

    def exit_window(self):
        self.sold_products_window.destroy()





app = CTk()
app.geometry('1700x900')
app.config(background='lemonchiffon1')

HeadingLabel = Label(app, text='Morya Electronics', font=('URW Bookman L', 50, 'italic'), foreground='black', background='burlywood1')
HeadingLabel.pack(fill=X)

Second_row = Frame(app, background='lemonchiffon1')
Second_row.pack()

buttonsFrame = Frame(Second_row, background='lemonchiffon1')
buttonsFrame.grid(row=0, column=0)

sellButton = CTkButton(buttonsFrame, text='Sell Product', command=sell_py, height=380, width=380, font=('URW Gothic L', 40), fg_color='slateblue4', text_color='white', hover_color='slateblue3', border_width=5)
sellButton.grid(row=0, column=0, padx=10, pady=10)

buyButton = CTkButton(buttonsFrame, text='Buy Product', command=buy_py, height=380,width=380,font=('URW Gothic L', 40),fg_color='#308014', text_color='white', hover_color='#00CD66', border_width=5)
buyButton.grid(row=0, column=1)

InventoryButton = CTkButton(buttonsFrame, text='Inventory', command=inventory_py, height=380,width=380,font=('URW Gothic L', 40),fg_color='tomato4', text_color='white', hover_color='tomato3', border_width=5)
InventoryButton.grid(row=1, column=0)

soldProductsButton = CTkButton(buttonsFrame, text='Sold Products', command=sold_py, height=380,width=380,font=('URW Gothic L', 40),fg_color='purple', text_color='white', hover_color='mediumorchid3', border_width=5)
soldProductsButton.grid(row=1, column=1)

Img_Frame = Frame(Second_row, background='lemonchiffon1')
Img_Frame.grid(row=0, column=1)

# new_label = Label(Img_Frame, text='qwertyujk')
# new_label.grid(row=0, column=0)
welcome_image = PhotoImage(file='welcome-38235.png')
Welcome_img_label = Label(Img_Frame, image=welcome_image, background='lemonchiffon1')
Welcome_img_label.grid(row=0, column=0, padx=10)


app.mainloop()