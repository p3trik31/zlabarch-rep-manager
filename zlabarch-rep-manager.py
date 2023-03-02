import tkinter as tk
from tkinter import ttk
import argparse
import os
import getpass
import base64

REPO_FILE_PATH = '/pokus/zlarch-repo'
PASSWORD_FILE_PATH = '/etc/zlabarch-rep-manager/admin_password.txt'



def list_pkg_files(path):
    pkg_files = []
    for filename in os.listdir(path):
        if filename.endswith(".pkg.tar.zst"):
            base_filename = os.path.splitext(filename)[0]
            pkg_files.append(base_filename)
    return pkg_files

def create_gui():
    gui = True
    
    #hlavni okno
    window = tk.Tk()
    window.title("Zlabarch-rep-manager")
    
    # top panel
    top_panel = tk.Frame(window, bg="#263238", height=50)
    top_panel.pack(side="top", fill="x")
    
    #rozpoznani ve kterem modu je aplikace spustena
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
        
    
    # middle panel
    middle_panel = tk.Frame(window, bg="#CFD8DC")
    middle_panel.pack(side="top", fill="both", expand=True)
    
    # listbox pro unchecked 
    unchecked_label = tk.Label(middle_panel, text="Unchecked Packages", font=("Helvetica", 12, "bold"), bg="#CFD8DC")
    unchecked_label.pack(side="left", padx=10, pady=10)
    unchecked_listbox = tk.Listbox(middle_panel, selectmode="multiple", bg="white", fg="#263238", font=("Helvetica", 12))
    unchecked_listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    # listbox pro balicky
    packages_label = tk.Label(middle_panel, text="Packages", font=("Helvetica", 12, "bold"), bg="#CFD8DC")
    packages_label.pack(side="left", padx=10, pady=10)
    packages_listbox = tk.Listbox(middle_panel, selectmode="multiple", bg="white", fg="#263238", font=("Helvetica", 12))
    packages_listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    pkg_files = list_pkg_files(REPO_FILE_PATH)
    for filename in pkg_files:
        packages_listbox.insert(tk.END, filename)
    
    
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
    password = getpass.getpass(prompt='Zadejte nové heslo pro admin pravomoce: ')
    confirm_password = getpass.getpass(prompt='Potvrdit heslo: ')
    while password != confirm_password:
        print('Hesla se neschodují, zkuste to znovu.')
        password = getpass.getpass(prompt='Zadejte nové heslo pro admin pravomoce ')
        confirm_password = getpass.getpass(prompt='Potvrdit heslo: ')
    with open(PASSWORD_FILE_PATH, 'w') as f:
        f.write(password)
    print(f'Heslo bylo vytvořeno')

def check_admin_password():
    if not os.path.exists(PASSWORD_FILE_PATH):
        create_password_file()
    else:
        with open(PASSWORD_FILE_PATH, 'r') as f:
            password = f.read().strip()
        if not password:
            print('Vytvořte heslo nové heslo pro admin pravomoce')
            create_password_file()
        else:
            input_password = getpass.getpass(prompt='Zadejte admin heslo: ')
            while input_password != password:
                print('Nesprávné heslo, zkuste to znovu')
                input_password = getpass.getpass(prompt='Zadejte admin heslo: ')

parser = argparse.ArgumentParser()

# admin argument
parser.add_argument('-a', '--admin', action='store_true', help='Zapnutí aplikace s admin pravomocemi')
parser.add_argument('-e', '--repo-edit', action='store_true', help='repo dir')

subparsers = parser.add_subparsers(title='commands', dest='command')

# Add argument
add_parser = subparsers.add_parser('add', help='Přidání nového balíčku')
add_parser.add_argument('package', type=package_file, help='Balíček pro přidání')

# Del argument
del_parser = subparsers.add_parser('del', help='Vymazat balíček')
del_parser.add_argument('item', help='Balíček pro vymazání')

# Update argument
update_parser = subparsers.add_parser('update', help='Aktualizace balíčku')
update_parser.add_argument('item', help='Balíček pro aktualizaci')
update_parser.add_argument('new_value', help='Nová verze balíčku')


args = parser.parse_args()








if args.admin:
    check_admin_password()
    print('admin mode')
else:
    print('user mode')


if args.command == 'add':
    print(f'Přidáno: {args.package}...')
    
elif args.command == 'del':
    print(f'vymazáno:  {args.item}...')
elif args.command == 'update':
    print(f'Aktualizováno: {args.item} na {args.new_value}...')
else:
    create_gui()
