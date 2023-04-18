from tkinter import *                   
from tkinter import ttk as ttk          
from tkinter import messagebox as mb   
import datetime                        
import sqlite3                          
from tkcalendar import DateEntry       
 
# list all the expenses
def listAllExpenses():
    
    # global variables  
    global dbconnector, data_table  
    
    data_table.delete(*data_table.get_children())  
    
    all_data = dbconnector.execute('SELECT * FROM ExpenseTracker')  
    data = all_data.fetchall()  
    
    # inserting the values in the tkinter data table
    for val in data:  
        data_table.insert('', END, values = val)  

# view an expense information
def viewExpenseInfo():  
    
    # global variables
    global data_table  
    global dateField, payee, description, amount, paymentMethod  
    
    # error message box
    if not data_table.selection():  
        mb.showerror('No expense record selected', 'Please select an expense record from the table to view')  
    
    currentSelectedExpense = data_table.item(data_table.focus())  
    val = currentSelectedExpense['values']  
    expenditureDate = datetime.date(int(val[1][:4]), int(val[1][5:7]), int(val[1][8:]))  

    dateField.set_date(expenditureDate) ; payee.set(val[2]) ; description.set(val[3]) ; amount.set(val[4]) ; paymentMethod.set(val[5])  

# clear the entries from the entry fields
def clearFields():  
    
    #global variable
    global description, payee, amount, paymentMethod, dateField, data_table  
  
    todayDate = datetime.datetime.now().date()  
  
    description.set('') ; payee.set('') ; amount.set(0.0) ; paymentMethod.set('Cash'), dateField.set_date(todayDate)  
    data_table.selection_remove(*data_table.selection())  

# remove the selected expense
def removeExpense():  
    
    # error message box
    if not data_table.selection():  
        mb.showerror('No expense record selected!', 'Please select a expense record to remove!', icon='warning')  
        return  
  
    currentSelectedExpense = data_table.item(data_table.focus())  

    valuesSelected = currentSelectedExpense['values']  
    
    # message box when the user hit the button
    confirmation = mb.askyesno('Confirmation', 'Are you sure that you want to remove the record of {valuesSelected[2]}')  
  
    if confirmation:  
        dbconnector.execute('REMOVE FROM ExpenseTracker WHERE ID=%d' % valuesSelected[0])  
        dbconnector.commit()  
        listAllExpenses()  
        mb.showinfo('Expense removed successfully!', 'The record you wanted to remove has been removed successfully')  

# delete all the entries
def removeAllExpenses():  
    confirmation = mb.askyesno('Confirmation', f'Are you sure that you want to remove all the expense items from the database?', icon='warning')  
  
    if confirmation:  
        data_table.delete(*data_table.get_children())  
        dbconnector.execute('REMOVE FROM ExpenseTracker')  
        dbconnector.commit()  
        clearFields()  
        listAllExpenses()  
        # message for successfullt remove the expense from database
        mb.showinfo('All Expenses has been removed!', 'All the expenses were successfully removed!')  
    else: 
        # message for cancel the request to remove all expenses
        mb.showinfo('Confirmation', 'Removed all expenses request has been cancelled!')  

# add an expense
def addAnotherExpense():    
    
    # global variables
    global dateField, payee, description, amount, paymentMethod 
    global dbconnector  
    
    # error message box
    if not dateField.get() or not payee.get() or not description.get() or not amount.get() or not paymentMethod.get():  
        mb.showerror('Fields are empty!', "Please fill all the missing fields then hit the 'Add Expense' button!")  
    else:  
        dbconnector.execute(  
            'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, paymentMethod) VALUES (?, ?, ?, ?, ?)',  
            (dateField.get_date(), payee.get(), description.get(), amount.get(), paymentMethod.get())  
        )  
        dbconnector.commit()  
        clearFields()  
        listAllExpenses()
        
        # message box when the user hit the button
        mb.showinfo('Expense added', 'The expense whose details you just entered has been added to the database')  

# edit expense
def editExpense():  
    # global variable
    global data_table  
  
    def editExistingExpense():  
        
        # global variable
        global dateField, amount, description, payee, paymentMethod  
        global dbconnector, data_table  
          
        currentSelectedExpense = data_table.item(data_table.focus())  
          
        content = currentSelectedExpense['values']  
        
        # update the information to database
        dbconnector.execute(  
            'UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, paymentMethod = ? WHERE ID = ?',  
            (dateField.get_date(), payee.get(), description.get(), amount.get(), paymentMethod.get(), content[0])  
        )  
        dbconnector.commit()  
        clearFields()  
        listAllExpenses()  
          
        mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')  
        editSelectedButton.destroy()  
    
    # if no expense is selectted, returning a error message box
    if not data_table.selection():  
        mb.showerror('No expense selected!', 'You have not selected any expense in the table for us to edit; please do that!')  
        return  
          
    viewExpenseInfo()  
    
    # edit button
    editSelectedButton = Button(  
        frameL3,  
        text = "Edit Expense",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 30,  
        bg = "#90EE90",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#008000",  
        activeforeground = "#98FB98",  
        command = editExistingExpense  
        )  
  
    editSelectedButton.grid(row = 0, column = 0, sticky = W, padx = 50, pady = 10)  

# main function
if __name__ == "__main__":  
  
    # connecting to the database
    dbconnector = sqlite3.connect("Budget Budget Budget.db")  
    dbcursor = dbconnector.cursor()  
  
    dbconnector.execute(  
        'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, paymentMethod TEXT)'  
    )  
    dbconnector.commit()  
  
    # setting for the app pop up window
    main_win = Tk()  
    main_win.title("BUDGET BUDGET BUDGET")  
    main_win.geometry("1440x600+400+100")  
    main_win.resizable(0, 0)  
    main_win.config(bg = "#FFFAF0")  
    
    # custom frames
    frameLeft = Frame(main_win, bg = "#80ced6")  
    frameRight = Frame(main_win, bg = "#DEB887")  
    frameL1 = Frame(frameLeft, bg = "#80ced6")  
    frameL2 = Frame(frameLeft, bg = "#80ced6")  
    frameL3 = Frame(frameLeft, bg = "#80ced6")  
    frameR1 = Frame(frameRight, bg = "#3e4444")  
    frameR2 = Frame(frameRight, bg = "#DEB887")  
  
    frameLeft.pack(side=LEFT, fill = "both")  
    frameRight.pack(side = RIGHT, fill = "both", expand = True)  
    frameL1.pack(fill = "both")  
    frameL2.pack(fill = "both")  
    frameL3.pack(fill = "both")  
    frameR1.pack(fill = "both")  
    frameR2.pack(fill = "both", expand = True)  
  
    # Heading lable
    headingLabel = Label(  
        frameL1,  
        text = "BUDGET BUDGET BUDGET",  
        font = ("Bahnschrift Condensed", "25"),  
        width = 20,  
        bg = "#82b74b",  
        fg = "#FFFAF0"  
        )  
    # second heading lable
    subheadingLabel = Label(  
        frameL1,  
        text = "SAVE MONEY    SAVE LIFE",  
        font = ("Bahnschrift Condensed", "15"),  
        width = 20,  
        bg = "#405d27",  
        fg = "#000000"  
        )  
  
    headingLabel.pack(fill = "both")  
    subheadingLabel.pack(fill = "both")  
  
    # input labels
    dateLabel = Label(  
        frameL2,  
        text = "Date:",  
        font = ("consolas", "12", "bold"),  
        bg = "#80ced6",  
        fg = "#000000"  
        )  

    descriptionLabel = Label(  
        frameL2,  
        text = "Description:",  
        font = ("consolas", "12", "bold"),  
        bg = "#80ced6",  
        fg = "#000000"  
        )  
  
    amountLabel = Label(  
        frameL2,  
        text = "Amount:",  
        font = ("consolas", "12", "bold"),  
        bg = "#80ced6",  
        fg = "#000000"  
        )  
  
    payeeLabel = Label(  
        frameL2,  
        text = "Payee:",  
        font = ("consolas", "12", "bold"),  
        bg = "#80ced6",  
        fg = "#000000"  
        )  
  
    paymentLabel = Label(  
        frameL2,  
        text = "Payment Method:",  
        font = ("consolas", "12", "bold"),  
        bg = "#80ced6",  
        fg = "#000000"  
        )  
  
    dateLabel.grid(row = 0, column = 0, sticky = W, padx = 10, pady = 10)      
    descriptionLabel.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 10)      
    amountLabel.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 10)      
    payeeLabel.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 10)      
    paymentLabel.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 10)      
    
    # input types
    description = StringVar()  
    payee = StringVar()  
    paymentMethod = StringVar(value = "Cash")  
    amount = DoubleVar()  
    
    # date input
    dateField = DateEntry(  
        frameL2,  
        date = datetime.datetime.now().date(),  
        font = ("consolas", "11"),  
        relief = GROOVE  
        )  
    # description input
    descriptionField = Entry(  
        frameL2,  
        text = description,  
        width = 20,  
        font = ("consolas", "11"),  
        bg = "#FFFFFF",  
        fg = "#000000",  
        relief = GROOVE  
        )  
    # amount of money input
    amountField = Entry(  
        frameL2,  
        text = amount,  
        width = 20,  
        font = ("consolas", "11"),  
        bg = "#FFFFFF",  
        fg = "#000000",  
        relief = GROOVE  
        )  
    # payee input
    payeeField = Entry(  
        frameL2,  
        text = payee,  
        width = 20,  
        font = ("consolas", "11"),  
        bg = "#FFFFFF",  
        fg = "#000000",  
        relief = GROOVE  
        )  
    
    # payment input
    paymentField = OptionMenu(  
        frameL2,  
        paymentMethod,  
        *['Cash', 'Credit Card', 'Debit Card', 'Google Pay', 'Apple Pay', 'PayPal']  
        )  
    paymentField.config(  
        width = 15,  
        font = ("consolas", "10"),  
        relief = GROOVE,  
        bg = "#FFFFFF"  
        )  
  
    dateField.grid(row = 0, column = 1, sticky = W, padx = 10, pady = 10)  
    descriptionField.grid(row = 1, column = 1, sticky = W, padx = 10, pady = 10)  
    amountField.grid(row = 2, column = 1, sticky = W, padx = 10, pady = 10)  
    payeeField.grid(row = 3, column = 1, sticky = W, padx = 10, pady = 10)  
    paymentField.grid(row = 4, column = 1, sticky = W, padx = 10, pady = 10)  
  
    # function buttons under the inputs
    insertButton = Button(  
        frameL3,  
        text = "Add Expense",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 30,  
        bg = "#90EE90",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#008000",  
        activeforeground = "#98FB98",  
        command = addAnotherExpense
        )  

    resetButton = Button(  
        frameL3,  
        text = "Clear The Fields",  
        font = ("Bahnschrift Condensed", "13"),  
        width = 30,  
        bg = "#FF0000",  
        fg = "#FFFFFF",  
        relief = GROOVE,  
        activebackground = "#8B0000",  
        activeforeground = "#FFB4B4",  
        command = clearFields
        )  
  
    insertButton.grid(row = 0, column = 0, sticky = W, padx = 50, pady = 30)  
    resetButton.grid(row = 1, column = 0, sticky = W, padx = 50, pady = 30)
  
    # function buttons on top of the table
    viewButton = Button(  
        frameR1,  
        text = "View Selected Expense",  
        font = ("Bahnschrift Condensed", "14"),  
        width = 30,  
        bg = "#92a8d1",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#A0522D",  
        activeforeground = "#FFF8DC",  
        command = viewExpenseInfo
        )  
  
    editButton = Button(  
        frameR1,  
        text = "Edit Selected Expense",  
        font = ("Bahnschrift Condensed", "14"),  
        width = 30,  
        bg = "#92a8d1",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#A0522D",  
        activeforeground = "#FFF8DC",  
        command = editExpense
        )  
  
    deleteButton = Button(  
        frameR1,  
        text = "Remove Selected Expense",  
        font = ("Bahnschrift Condensed", "14"),  
        width = 30,  
        bg = "#92a8d1",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#A0522D",  
        activeforeground = "#FFF8DC",  
        command = removeExpense
        )  
      
    deleteAllButton = Button(  
        frameR1,  
        text = "Remove All Expenses",  
        font = ("Bahnschrift Condensed", "14"),  
        width = 30,  
        bg = "#92a8d1",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#A0522D",  
        activeforeground = "#FFF8DC",  
        command = removeAllExpenses 
        )  
    
    # set up UI for fucntion buttons
    viewButton.grid(row = 0, column = 0, sticky = W, padx = 10, pady = 10)  
    editButton.grid(row = 0, column = 1, sticky = W, padx = 10, pady = 10)  
    deleteButton.grid(row = 0, column = 2, sticky = W, padx = 10, pady = 10)  
    deleteAllButton.grid(row = 0, column = 3, sticky = W, padx = 10, pady = 10)  
  
    # data table column labels
    data_table = ttk.Treeview(  
        frameR2,  
        selectmode = BROWSE,  
        columns = ('ID', 'Date', 'Payee', 'Description', 'Amount', 'Payment Method')  
        )  
  
    # scrollbar for horizontal
    Xaxis_Scrollbar = Scrollbar(  
        data_table,  
        orient = HORIZONTAL,  
        command = data_table.xview  
        ) 
    
    # scrollbar for vertical
    Yaxis_Scrollbar = Scrollbar(  
        data_table,  
        orient = VERTICAL,  
        command = data_table.yview  
        )  
  
    Xaxis_Scrollbar.pack(side = BOTTOM, fill = X)  
    Yaxis_Scrollbar.pack(side = RIGHT, fill = Y)  
  
    data_table.config(yscrollcommand = Yaxis_Scrollbar.set, xscrollcommand = Xaxis_Scrollbar.set)  
    
    # data table headings
    data_table.heading('ID', text = 'ID', anchor = CENTER)  
    data_table.heading('Date', text = 'Date', anchor = CENTER)  
    data_table.heading('Payee', text = 'Payee', anchor = CENTER)
    data_table.heading('Description', text = 'Description', anchor = CENTER)  
    data_table.heading('Amount', text = 'Amount', anchor = CENTER)  
    data_table.heading('Payment Method', text = 'Payment Method', anchor = CENTER)  
  
    # data table column width for every elements
    data_table.column('#0', width = 0, stretch = NO)  
    data_table.column('#1', width = 50, stretch = NO)  
    data_table.column('#2', width = 95, stretch = NO)  
    data_table.column('#3', width = 200, stretch = NO)  
    data_table.column('#4', width = 450, stretch = NO)  
    data_table.column('#5', width = 135, stretch = NO)  
    data_table.column('#6', width = 140, stretch = NO)  
  
    data_table.place(relx = 0, y = 0, relheight = 1, relwidth = 1)  
    main_win.mainloop()