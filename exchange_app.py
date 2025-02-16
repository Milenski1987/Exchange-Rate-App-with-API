from tkinter import StringVar, OptionMenu
from tkinter.constants import SUNKEN
import requests
import tkinter as tk
from currencies_data import supported_currency


def exchange(current_currency:str,current_currency_amount: int, wanted_currency:str) -> tuple:

    # Making our request and get information
    url = f'https://v6.exchangerate-api.com/v6/{enter_your_api_key_here}/latest/{current_currency}'
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
root.geometry("500x350")


#create currency type input field
input_field_label_type = tk.Label(root, text="Choose code of the currency you want to exchange here:")
input_currency_menu = StringVar(root)
input_currency_menu.set(supported_currency[0])
input_menu = OptionMenu(root, input_currency_menu, *supported_currency)
input_field_label_type.pack()
input_menu.pack()

#create received currency input field
input_field_label_receive = tk.Label(root, text="Choose code of the currency you want to receive here:")
input_receive_menu = StringVar(root)
input_receive_menu.set(supported_currency[0])
receive_menu = OptionMenu(root, input_receive_menu, *supported_currency)
input_field_label_receive.pack()
receive_menu.pack()


#create currency amount input field
input_field_label_amount = tk.Label(root, text="How much of the currency you want to exchange(integer without decimal point):")
input_field_entry_amount = tk.Entry(root,justify='center', bg="black", fg="white")
input_field_label_amount.pack()
input_field_entry_amount.pack()


#create exchange button
exchange_button = tk.Button(root, text="Exchange", command=lambda: get_exchange_information())

exchange_button.pack()

#create app response field
response_field = tk.Text(root, bg="black", fg="yellow", height= 50)
response_field.pack()

def get_exchange_information():
    user_current_currency = input_currency_menu.get()
    user_wanted_currency = input_receive_menu.get()
    user_current_currency_amount = int(input_field_entry_amount.get())

    response = exchange(user_current_currency, user_current_currency_amount, user_wanted_currency)

    response_field.insert(tk.END, response)

root.mainloop()
main()