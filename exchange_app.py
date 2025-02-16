from tkinter import StringVar, OptionMenu
from tkinter.constants import SUNKEN
import requests
import tkinter as tk
from currencies_data import supported_currency


def exchange(current_currency:str,current_currency_amount: int, wanted_currency:str) -> tuple:

    # Making our request and get information
    url = f'https://v6.exchangerate-api.com/v6/{enter_api_key_here}/latest/{current_currency}'
    response = requests.get(url)
    rate = response.json()["conversion_rates"][wanted_currency]
    current_result = rate * current_currency_amount
    return (f"Current exchange rate: 1 {current_currency} = {rate:.3f} {wanted_currency}\n"
            f"For {current_currency_amount} {current_currency.upper()} "
            f"you will receive {current_result:.3f} {wanted_currency.upper()}\n\n")


def main():
    print("Hello to Exchange Rate App")

    #User choose what currency to exchange and amount of that currency
    user_current_currency = input("Please enter 3 letters code of the currency you want to exchange:  ")
    user_current_currency_amount = int(input("How much of the currency you want to exchange:  "))

    #User choose what currency to receive
    user_wanted_currency = input("Please enter 3 letters code of the currency you want to receive:  ")

    #User get information about exchange rate and amount of currency he will receive
    result = exchange(user_current_currency.upper(),user_current_currency_amount, user_wanted_currency.upper())
    print(result)


root = tk.Tk()
root.title("Exchange rate App")
root.geometry("515x300")


#create labels
input_field_label_type = tk.Label(root, text="Choose code of the currency you want to exchange here:")
input_field_label_receive = tk.Label(root, text="Choose code of the currency you want to receive here:")

#arrange labels
input_field_label_type.grid(row=0, column=0, sticky="w")
input_field_label_receive.grid(row=1, column=0, sticky="w")

#create menus
input_currency_menu = StringVar(root)
input_currency_menu.set(supported_currency[0])
input_menu = OptionMenu(root, input_currency_menu, *supported_currency)
input_menu.config(fg="black")
input_receive_menu = StringVar(root)
input_receive_menu.set(supported_currency[0])
receive_menu = OptionMenu(root, input_receive_menu, *supported_currency)
receive_menu.config(fg="black")

#arrange menus
input_menu.grid(row=0, column= 1, sticky="")
receive_menu.grid(row=1, column= 1, sticky="")

#create amount entry label and arrange it
input_field_label_amount = tk.Label(root, text="Currency amount you want to exchange(integer without decimal point):")
input_field_label_amount.grid(row=2,column = 0, sticky="w")

#create amount entry field and arrange it
input_field_entry_amount = tk.Entry(root,justify='center', bg="black", fg="white", width=7)
input_field_entry_amount.grid(row=2,column= 1, sticky="")

#create exchange button and arrange it
exchange_button = tk.Button(root, text="Exchange", command=lambda: get_exchange_information())
exchange_button.grid(row=3,column=0,sticky="",columnspan = 2)


#create app response field and arrange it
response_field = tk.Text(root, bg="black", fg="white", width= 70, height= 14)
response_field.grid(row=4,column=0,columnspan = 2)

def get_exchange_information():
    user_current_currency = input_currency_menu.get()
    user_wanted_currency = input_receive_menu.get()
    user_current_currency_amount = int(input_field_entry_amount.get())
    response = exchange(user_current_currency, user_current_currency_amount, user_wanted_currency)

    response_field.insert(tk.END, response)

root.mainloop()
main()