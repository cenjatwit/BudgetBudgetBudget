# importing the required modules  
from tkinter import *                   # importing all the modules and classes from tkinter  
from tkinter import ttk as ttk          # importing the ttk module from tkinter  
from tkinter import messagebox as mb    # importing the messagebox module from tkinter  
import datetime                         # importing the datetime module  
import sqlite3                          # importing the sqlite3 module  
#from tkcalendar import DateEntry        # importing the DateEntry class from the tkcalendar module  
  
# function to list all the expenses  
def listAllExpenses():  
    '''''This function will retrieve the data from the database and insert it to the tkinter data table'''  
  
    global dbconnector, data_table  
    # clearing the table  
    data_table.delete(*data_table.get_children())  
    all_data = dbconnector.execute('SELECT * FROM ExpenseTracker')  
  
    data = all_data.fetchall()  
      
    for val in data:  
        data_table.insert('', END, values = val)  
  
# function to view an expense information  
def viewExpenseInfo():  
    '''''This function will display the expense information in the data frame'''  
  
    global data_table  
    global dateField, payee, description, amount, modeOfPayment  
  
    if not data_table.selection():  
        mb.showerror('No expense selected', 'Please select an expense from the table to view its details')  
  
    currentSelectedExpense = data_table.item(data_table.focus())  
  
    val = currentSelectedExpense['values']  
  
    expenditureDate = datetime.date(int(val[1][:4]), int(val[1][5:7]), int(val[1][8:]))  
  
    dateField.set_date(expenditureDate) ; payee.set(val[2]) ; description.set(val[3]) ; amount.set(val[4]) ; modeOfPayment.set(val[5])  
  
# function to clear the entries from the entry fields  
def clearFields():  
    '''''This function will clear all the entries from the entry fields'''  
  
    global description, payee, amount, modeOfPayment, dateField, data_table  
  
    todayDate = datetime.datetime.now().date()  
  
    description.set('') ; payee.set('') ; amount.set(0.0) ; modeOfPayment.set('Cash'), dateField.set_date(todayDate)  
    data_table.selection_remove(*data_table.selection())  
  
# function to delete the selected record  
def removeExpense():  
    '''''This function will remove the selected record from the table'''  
  
    if not data_table.selection():  
        mb.showerror('No record selected!', 'Please select a record to delete!')  
        return  
  
    currentSelectedExpense = data_table.item(data_table.focus())  
  
    valuesSelected = currentSelectedExpense['values']  
  
    confirmation = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {valuesSelected[2]}')  
  
    if confirmation:  
        dbconnector.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % valuesSelected[0])  
        dbconnector.commit()  
  
        listAllExpenses()  
  
        mb.showinfo('Record deleted successfully!', 'The record you wanted to delete has been deleted successfully')  
  
# function to delete all the entries  
def removeAllExpenses():  
    '''''This function will remove all the entries from the table'''  
      
    confirmation = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the expense items from the database?', icon='warning')  
  
    if confirmation:  
        data_table.delete(*data_table.get_children())  
  
        dbconnector.execute('DELETE FROM ExpenseTracker')  
        dbconnector.commit()  
  
        clearFields()  
  
        listAllExpenses()  
  
        mb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')  
    else:  
        mb.showinfo('Ok then', 'The task was aborted and no expense was deleted!')  