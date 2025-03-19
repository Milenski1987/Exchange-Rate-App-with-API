import requests
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def check_input_validity(func):
    # Check for positive number
    def wrapper(current_currency_amount, *args, **kwargs):
        if current_currency_amount <= 0:
            raise ValueError
        return func(current_currency_amount, *args, **kwargs)
    return wrapper

@check_input_validity
def exchange(current_currency_amount: float,current_currency:str, wanted_currency:str) -> str:
    # Making our request and getting information
    try:
        url = f'https://v6.exchangerate-api.com/v6/<YOUR_API_KEY>/latest/{current_currency.split()[1]}'
        response = requests.get(url)
        rate = response.json()["conversion_rates"][wanted_currency.split()[1]]
        current_result = rate * current_currency_amount
    except KeyError:
        return "Server error! Please try again later!"
    else:
        return (f"Current exchange rate:\n1 {current_currency.split()[1]} = {rate:.3f}{wanted_currency.split()[1]}\n\n"
                f"For {current_currency_amount:.3f} {current_currency.split()[1]}\n "
                f"you will receive {current_result:.3f} {wanted_currency.split()[1]}\n\n")

def get_exchange_information():
    # main GUI function that gives user a choice for currencies and amount
    try:
        response_field.delete("1.0", "end")
        user_current_currency = input_currency_menu.get()
        user_wanted_currency = input_receive_menu.get()
        user_current_currency_amount = float(input_field_entry_amount.get())
        response = exchange( user_current_currency_amount,user_current_currency, user_wanted_currency)
        response_field.insert(tk.END, response)
    except ValueError:
        response_field.insert(tk.END, "Amount must be valid positive number")

def dashboard_rates(first_currency:str) -> float:
    # Get information for our dashboard with common currencies
    url = f'https://v6.exchangerate-api.com/v6/<YOUR_API_KEY>/latest/{first_currency}'
    response = requests.get(url)
    rate_usd = response.json()["conversion_rates"]["USD"]
    rate_gbp = response.json()["conversion_rates"]["GBP"]
    rate_chf = response.json()["conversion_rates"]["CHF"]
    rate_bgn = response.json()["conversion_rates"]["BGN"]
    rate_cny = response.json()["conversion_rates"]["CNY"]
    return rate_usd, rate_gbp, rate_chf, rate_bgn, rate_cny

def information_pop_up():
    #Create screen with detailed information about currencies
    informative_screen = Toplevel()
    informative_screen.geometry("1000x690")
    informative_screen.title("Detailed information")
    imagebox = tk.Label(informative_screen)
    imagebox.pack()
    codes_file = os.path.join("images", "currency_codes.png")
    image = ImageTk.PhotoImage(file=resource_path(codes_file))
    imagebox.config(image=image)
    imagebox.image = image

def toggle():
    #Creates toggle between light and dark modes
    global switch_value
    if switch_value == True:
        my_canvas.create_image(0,0,image = dark, anchor="nw")
        my_canvas.create_text(450, 260, text="Choose the currency you want to exchange here: ", font=("Arial", 15),
                              fill="white")
        my_canvas.create_text(450, 320, text="Choose the currency you want to receive here:", font=("Arial", 15),
                              fill="white")
        my_canvas.create_text(450, 385, text="Currency amount you want to exchange: ", font=("Arial", 15), fill="white")
        my_canvas.create_text(800, 53, text="For more detailed currency information: ", font=("Arial", 15),
                              fill="white")
        input_menu.config(bg="black", fg="white", width=25)
        receive_menu.config(bg="black", fg="white", width=25)
        input_field_entry_amount.config(justify='center', bg="grey", fg="white")
        dashboard_text.config(bg="black", fg="white", font="Arial")
        response_field.config(bg="black", fg="white")
        my_canvas.create_text(790, 140, text="For 'light mode' click here:", font=("Arial", 15), fill="white")
        switch.config(text="Light mode")
        switch_value = False
    else:
        my_canvas.create_image(0,0,image = light, anchor="nw")
        my_canvas.create_text(450, 260, text="Choose the currency you want to exchange here: ", font=("Arial", 15),
                              fill="black")
        my_canvas.create_text(450, 320, text="Choose the currency you want to receive here:", font=("Arial", 15),
                              fill="black")
        my_canvas.create_text(450, 385, text="Currency amount you want to exchange: ", font=("Arial", 15), fill="black")
        my_canvas.create_text(800, 53, text="For more detailed currency information: ", font=("Arial", 15),
                              fill="black")
        input_menu.config(bg="light blue", fg="black", width=25)
        receive_menu.config(bg="light blue", fg="black", width=25)
        input_field_entry_amount.config(justify='center', bg="light blue", fg="black")
        dashboard_text.config(bg="light yellow", fg="black", font="Arial")
        response_field.config(bg="light blue", fg="black")
        my_canvas.create_text(790, 140, text="For 'dark mode' click here:", font=("Arial", 15), fill="black")
        switch.config(text="Dark mode")
        switch_value = True

def main():
    print("Hello to Exchange Rate App")

    #User choose what currency to exchange and amount of that currency
    user_current_currency = input("Please enter 3 letters code of the currency you want to exchange:  ")
    user_current_currency_amount = float(input("How much of the currency you want to exchange:  "))

    #User choose what currency to receive
    user_wanted_currency = input("Please enter 3 letters code of the currency you want to receive:  ")

    #User get information about exchange rate and amount of currency he will receive
    result = exchange(user_current_currency.upper(),user_current_currency_amount, user_wanted_currency.upper())
    print(result)

# read file with currencies data
currencies_data_file = os.path.join("resources", "currencies_data_for_mac.txt")
with open(resource_path(currencies_data_file), "r") as data_currency:
    supported_currency = data_currency.readlines()
    available_currencies = [currency.strip("\n") for currency in supported_currency]

#create GUI
root = tk.Tk()
root.title("Exchange rate App")
root.geometry("1020x690")

#define image
light_file = os.path.join("images", "official_background.png")
dark_file = os.path.join("images", "dark_background.png")
light = PhotoImage(file=resource_path(light_file))
dark = PhotoImage(file=resource_path(dark_file))
switch_value = True

#create canvas
my_canvas = tk.Canvas(root, width=1020, height=680)
my_canvas.pack(fill="both", expand=True)

#switch button to toggle light and dark mode
switch = ttk.Button(root, command=toggle)
switch.config(text="Dark mode")
switch.place(x= 735, y = 150)

#set image in canvas
my_canvas.create_image(0,0,image = light, anchor="nw")

#create labels for input fields
my_canvas.create_text(450,260 , text="Choose the currency you want to exchange here: ",font=("Arial", 15), fill="black")
my_canvas.create_text(450,320 , text="Choose the currency you want to receive here:",font=("Arial", 15), fill="black")
my_canvas.create_text(450,385 , text="Currency amount you want to exchange: ",font=("Arial", 15), fill="black")
my_canvas.create_text(790,140 , text="For 'dark mode' click here:",font=("Arial", 15), fill="black")

#create menus
input_currency_menu = StringVar(my_canvas)
input_currency_menu.set(" ")
input_menu = OptionMenu(my_canvas, input_currency_menu, *available_currencies)
input_menu.config(bg="light blue",fg="black",width=25)
input_receive_menu = StringVar(my_canvas)
input_receive_menu.set(" ")
receive_menu = OptionMenu(my_canvas, input_receive_menu, *available_currencies)
receive_menu.config(bg="light blue",fg="black",width=25)

#arrange menus
input_menu.place(x= 320, y= 275)
receive_menu.place(x= 320, y = 335)

#create amount entry field and arrange it
input_field_entry_amount = tk.Entry(my_canvas, width=10)
input_field_entry_amount.config(justify='center', bg="light blue", fg="black")
input_field_entry_amount.place(x= 400, y= 400)

#create exchange button and arrange it
style = ttk.Style()
style.configure("TButton", padding=0,bordercolor="lightblue", background="#ADD8E6", borderwidth=0)
exchange_button = ttk.Button(root,width= 15, text ="Exchange", command=lambda: get_exchange_information())
exchange_button.place(x = 360, y = 430)

#create app response field and arrange it
response_field = tk.Text(my_canvas, width=44, height= 11)
response_field.config(bg="light blue" , fg="black")
response_field.place(x = 290, y = 470)

#create and arrange dashboard with most common currencies
dashboard_text = tk.Text(my_canvas ,width= 28, height=8)
dashboard_text.config(bg="light yellow", fg="black", font="Arial")
try:
    rate_usd, rate_gbp, rate_chf, rate_bgn, rate_cny = dashboard_rates("EUR")
    dashboard_text.insert(tk.END, f"Common currencies rates for 🇪🇺Euro\n                         We Buy | We Sell")
    dashboard_text.insert(tk.END, f"\n 🇺🇸US Dollar        {rate_usd:.3f} | {(rate_usd + 0.012):.3f}")
    dashboard_text.insert(tk.END, f"\n 🇬🇧British Pound  {rate_gbp:.3f} | {(rate_gbp + 0.011):.3f}")
    dashboard_text.insert(tk.END, f"\n 🇨🇭Swiss Franc    {rate_chf:.3f} | {(rate_chf + 0.012):.3f}")
    dashboard_text.insert(tk.END, f"\n 🇧🇬Bulgarian Lev  {rate_bgn:.3f} | {(rate_bgn + 0.010):.3f}")
    dashboard_text.insert(tk.END, f"\n 🇨🇳Chinese yuan  {rate_cny:.3f} | {(rate_cny + 0.015):.3f}")
except KeyError:
    dashboard_text.insert(tk.END, "Server error! Please try again later!")
dashboard_text.place(x= 340, y = 20)

#create button for pop-up informative window
my_canvas.create_text(800,53 , text="For more detailed currency information: ",font=("Arial", 15), fill="black")
informative_button = ttk.Button(my_canvas, width=15, text = " Click Here!", command= lambda: information_pop_up() )
informative_button.place(x= 705, y = 65)


root.mainloop()
main()
