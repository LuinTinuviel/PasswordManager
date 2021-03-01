from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

PASSWORD_BANK_PATH = "bank.json"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
               'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, string=password)
    pyperclip.copy(password)


# -------------------------- GLOBAL FUNCTIONS ----------------------------- #
def load_password_data(path=PASSWORD_BANK_PATH):
    with open(PASSWORD_BANK_PATH, "r") as data_file:
        data = json.load(data_file)
        return data


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    username = email_username_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "username": username,
            "password": password
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showwarning(title="Invalid data", message="Please don't leave any fields empty")
    else:
        try:
            data = load_password_data()
        except FileNotFoundError:
            print("Password bank not found / Creating New File")
            with open(PASSWORD_BANK_PATH, "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            print("Updating Bank file")
            # Update old data
            data.update(new_data)
            with open(PASSWORD_BANK_PATH, "w") as data_file:
                # Save updated data
                json.dump(data, data_file, indent=4)
        finally:
            print(f'Saved following data: {website} | {username} | {password}')
            clear_entries()


def clear_entries():
    website_entry.delete(0, END)
    password_entry.delete(0, END)


# ------------------------- SEARCH PASSWORD ---------------------------- #

def find_password():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showwarning(title="Empty website field", message="Write some website name first")
    else:
        try:
            data = load_password_data()
        except FileNotFoundError:
            messagebox.showwarning(title="Warning", message="No Data File Found")
        else:
            show_website_data(data, website)


def show_website_data(data, website):
    if website in data:
        username = data[website]["username"]
        password = data[website]["password"]
        message_to_show = f'Username: {username}\nPassword: {password}'
        messagebox.showinfo(title=website, message=message_to_show)
        pyperclip.copy(password)
    else:
        messagebox.showinfo(title="No Data Found", message="No details for this website")


# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title("Password Manager")
root.config(padx=50, pady=50)

# LOGO
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Label Website
website_label = Label(text="Website:", font=("Arial", 12))
website_label.grid(column=0, row=1)
# Label Email/Username
email_username_label = Label(text="Email/Username:", font=("Arial", 12))
email_username_label.grid(column=0, row=2)
# Label Password:
password_label = Label(text="Password:", font=("Arial", 12))
password_label.grid(column=0, row=3)

# Entry Website
website_entry = Entry(width=35)
website_entry.grid(column=1, row=1)
website_entry.focus()
# Entry Email/Username
email_username_entry = Entry(width=56)
email_username_entry.grid(column=1, row=2, columnspan=2)
email_username_entry.insert(END, string="miscoo@o2.pl")
# Entry Password
password_entry = Entry(width=35)
password_entry.grid(column=1, row=3)

# Search button
search_button = Button(text="Search", width="16", command=find_password)
search_button.grid(column=2, row=1)
# Generate button
generate_button = Button(text="Generate Password", width="16", command=password_generator)
generate_button.grid(column=2, row=3)
# Add button
add_button = Button(text="Add", width="47", command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

root.mainloop()
