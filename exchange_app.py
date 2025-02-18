import requests
import tkinter as tk
from tkinter import *


data_currency = open("currencies_data", "r")
supported_currency = data_currency.readlines()


def exchange(current_currency:str,current_currency_amount: int, wanted_currency:str) -> str:

    # Making our request and get information
    url = f'https://v6.exchangerate-api.com/v6/<YOUR_API_KEY_HERE>/latest/{current_currency.split("-")[0].strip()}'
    response = requests.get(url)
    rate = response.json()["conversion_rates"][wanted_currency.split("-")[0].strip()]
    current_result = rate * current_currency_amount
    return (f"Current exchange rate:\n1 {current_currency.split("-")[1]} = {rate:.3f}{wanted_currency.split("-")[1]}\n\n"
            f"For {current_currency_amount} {current_currency.split("-")[1]}\n "
            f"you will receive {current_result:.3f}{wanted_currency.split("-")[1]}\n\n")


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
root.geometry("800x480")

#define image
bg = PhotoImage(file="gettyimages-609801990.png")

#create canvas
my_canvas = tk.Canvas(root, width=800, height=480)
my_canvas.pack(fill="both", expand=True)

#set image in canvas
my_canvas.create_image(0,0,image = bg, anchor="nw")

#create labels
input_field_label_type = tk.Label(my_canvas,bg = "light yellow", text="Choose the currency you want to exchange here:")
input_field_label_receive = tk.Label(my_canvas,bg = "light yellow", text="Choose the currency you want to receive here:")

#arrange labels
input_field_label_type.place(x = 450, y = 10)
input_field_label_receive.place(x= 450, y = 90)

#create menus
input_currency_menu = StringVar(my_canvas)
input_currency_menu.set(supported_currency[0])
input_menu = OptionMenu(my_canvas, input_currency_menu, *supported_currency)
input_menu.config(bg="light blue",fg="black", pady =0, padx= 2)
input_receive_menu = StringVar(my_canvas)
input_receive_menu.set(supported_currency[0])
receive_menu = OptionMenu(my_canvas, input_receive_menu, *supported_currency)
receive_menu.config(bg="light blue",fg="black",pady=0)

#arrange menus
input_menu.place(x= 450, y= 35)
receive_menu.place(x= 450, y = 115)

#create amount entry label and arrange it
input_field_label_amount = tk.Label(my_canvas,bg = "light yellow", text="Currency amount you want to exchange:")
input_field_label_amount.place(x= 450, y = 170)

#create amount entry field and arrange it
input_field_entry_amount = tk.Entry(my_canvas,justify='center', bg="light blue", fg="black", width=36)
input_field_entry_amount.place(x= 450, y= 195)


#create exchange button and arrange it
exchange_button = tk.Button(my_canvas,bg="light blue", text="Exchange", command=lambda: get_exchange_information())
exchange_button.place(x = 570, y = 250)



#create app response field and arrange it
response_field = tk.Text(my_canvas, bg="light blue" , fg="black", width=48, height= 11)
response_field.place(x = 400, y = 280)

def get_exchange_information():
    user_current_currency = input_currency_menu.get()
    user_wanted_currency = input_receive_menu.get()
    user_current_currency_amount = int(input_field_entry_amount.get())
    response = exchange(user_current_currency, user_current_currency_amount, user_wanted_currency)

    response_field.insert(tk.END, response)

root.mainloop()
main()
