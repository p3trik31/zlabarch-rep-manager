import tkinter as tk
from tkinter import ttk
import argparse
import os
import getpass
import base64

REPO_FILE_PATH = '/etc/zlabarch-rep-manager/repo.txt'
PASSWORD_FILE_PATH = '/etc/zlabarch-rep-manager/admin_password.txt'




def create_gui():
    gui = True
    
    #hlavni okno
    window = tk.Tk()
    window.title("Package Manager")
    
    # create top panel
    top_panel = tk.Frame(window, bg="#263238", height=50)
    top_panel.pack(side="top", fill="x")
    
    
    if args.admin:
        admin_mode_label = ttk.Label(top_panel, text="Admin", background="#263238", foreground="white", font=("Helvetica", 16, "bold"))
        admin_mode_label.pack(side="left", padx=20, pady=10)
    else:
        user_mode_label = tk.Label(top_panel, text="User", bg="#263238", fg="white", padx=20, font=("Helvetica", 16, "bold"))
        user_mode_label.pack(side="left", padx=10, pady=10)
        
    #dropdown menu
    settings_menu = tk.StringVar()
    settings_menu.set("Nastavení")

    settings_dropdown = tk.OptionMenu(top_panel, settings_menu, "Změna emailu", "Změna hesla")
    settings_dropdown.config(font=("Helvetica", 12, "bold"), bg="#263238", fg="white", padx=10, pady=5, bd=0)
    settings_dropdown["menu"].config(bg="#263238", fg="white")
    settings_dropdown.pack(side="right", padx=10, pady=10)
        
    
    # create middle panel
    middle_panel = tk.Frame(window, bg="#CFD8DC")
    middle_panel.pack(side="top", fill="both", expand=True)
    
    # create unchecked packages listbox
    unchecked_label = tk.Label(middle_panel, text="Unchecked Packages", font=("Helvetica", 12, "bold"), bg="#CFD8DC")
    unchecked_label.pack(side="left", padx=10, pady=10)
    unchecked_listbox = tk.Listbox(middle_panel, selectmode="multiple", bg="white", fg="#263238", font=("Helvetica", 12))
    unchecked_listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    # create packages listbox
    packages_label = tk.Label(middle_panel, text="Packages", font=("Helvetica", 12, "bold"), bg="#CFD8DC")
    packages_label.pack(side="left", padx=10, pady=10)
    packages_listbox = tk.Listbox(middle_panel, selectmode="multiple", bg="white", fg="#263238", font=("Helvetica", 12))
    packages_listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    # button panel pro hlavni akce
    button_panel = tk.Frame(window, bg="#263238", height=50)
    button_panel.pack(side="top", fill="x")
    add_button = tk.Button(button_panel, text="Add", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5, bd=0)
    add_button.pack(side="left", padx=10, pady=10)
    del_button = tk.Button(button_panel, text="Del", font=("Helvetica", 12, "bold"), bg="#FF7043", fg="#263238", padx=10, pady=5, bd=0)
    del_button.pack(side="left", padx=10, pady=10)
    update_button = tk.Button(button_panel, text="Update", font=("Helvetica", 12, "bold"), bg="#FFB900", fg="#263238", padx=10, pady=5, bd=0)   
    update_button.pack(side="left", padx=10, pady=10)
    
    window.mainloop()



def package_file(file_path):
    if not file_path.endswith('.pkg.tar.zst'):
        raise argparse.ArgumentTypeError('Balíček musí být ve formátu.pkg.tar.zst')
    return file_path

def create_password_file():
    password = getpass.getpass(prompt='Enter a password for admin mode: ')
    confirm_password = getpass.getpass(prompt='Confirm the password: ')
    while password != confirm_password:
        print('Passwords do not match. Please try again.')
        password = getpass.getpass(prompt='Enter a password for admin mode: ')
        confirm_password = getpass.getpass(prompt='Confirm the password: ')
    with open(PASSWORD_FILE_PATH, 'w') as f:
        f.write(password)
    print(f'Password created successfully and saved to {PASSWORD_FILE_PATH}')

def check_admin_password():
    if not os.path.exists(PASSWORD_FILE_PATH):
        create_password_file()
    else:
        with open(PASSWORD_FILE_PATH, 'r') as f:
            password = f.read().strip()
        if not password:
            print('The password file is empty. Please create a password.')
            create_password_file()
        else:
            input_password = getpass.getpass(prompt='Enter the password for admin mode: ')
            while input_password != password:
                print('Incorrect password. Please try again.')
                input_password = getpass.getpass(prompt='Enter the password for admin mode: ')

# Define command-line arguments
parser = argparse.ArgumentParser()

# Add admin mode argument
parser.add_argument('-a', '--admin', action='store_true', help='Activate admin mode')
parser.add_argument('-e', '--repo-edit', action='store_true', help='repo dir')

# Add command argument and sub-commands
subparsers = parser.add_subparsers(title='commands', dest='command')

add_parser = subparsers.add_parser('add', help='Add a new package')
add_parser.add_argument('package', type=package_file, help='Package file to add')

# Add "del" sub-command
del_parser = subparsers.add_parser('del', help='Delete an item')
del_parser.add_argument('item', help='Item to delete')

# Add "update" sub-command
update_parser = subparsers.add_parser('update', help='Update an item')
update_parser.add_argument('item', help='Item to update')
update_parser.add_argument('new_value', help='New value for the item')

# Parse command-line arguments
args = parser.parse_args()







# Check if admin mode is activated
if args.admin:
    check_admin_password()
    print('Welcome to admin mode!')
else:
    print('user mode')

# Perform the requested command
if args.command == 'add':
    print(f'Adding {args.package}...')
    
elif args.command == 'del':
    print(f'Deleting {args.item}...')
elif args.command == 'update':
    print(f'Updating {args.item} to {args.new_value}...')
else:
    create_gui()
