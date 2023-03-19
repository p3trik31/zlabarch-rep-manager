import subprocess
import tkinter as tk
from tkinter import ttk
import argparse
import os
import getpass
import base64
from pathlib import Path
import keyring

def load_assets():
    print("")



REPO_FILE_PATH = '/pokus/zlarch-repo/'
REPO_PATH = '/pokus/zlarch-repo/'
ASSETS_PATH = Path(__file__).resolve().parent / "assets" #ikona a pozadi aplikace 


def add_pkg(path):     #přidání balíčku do repozitare
    try:                #funkce pouziva try a except
        subprocess.run(["repo-add", REPO_FILE_PATH, path], check=True)    #použije shell pro vykonání akce skrz subprocess modul
    except subprocess.CalledProcessError as err:
        print(f"chyba: {err}")

def del_pkg(package):   #Odebrání balíčku z repozitare
    try:                #funkce pouziva try a except
        subprocess.run(["repo-remove", REPO_FILE_PATH, package], check=True)    #použije shell pro vykonání akce skrz subprocess modul 
    except subprocess.CalledProcessError as err:
        print(f"chyba: {err}")

def update_pkg(old_path, new_path):
    print("")
    
    

def list_pkg_files(path):
    pkg_files = []
    for filename in os.listdir(path):
        if filename.endswith(".pkg.tar.zst"):
            base_filename = os.path.splitext(filename)[0]
            pkg_files.append(base_filename)
    return pkg_files


def select_path():
    global output_path

    output_path = tk.filedialog.askdirectory()
   # path_entry.delete(0, tk.END)
   # path_entry.insert(0, output_path)



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
    panelbackground = tk.PhotoImage(file=ASSETS_PATH / "background.png")
    middle_panel = tk.Frame(window, bg="#CFD8DC")
    middle_panel.pack(side="top", fill="both", expand=True)
    background_label = tk.Label(middle_panel, image=panelbackground)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    
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
#    update_button = tk.Button(button_panel, text="Update", font=("Helvetica", 12, "bold"), bg="#FFB900", fg="#263238", padx=10, pady=5, bd=0)   
#    update_button.pack(side="left", padx=10, pady=10)
    window.geometry("800x600")
    window.resizable(False, False)
    logo = tk.PhotoImage(file=ASSETS_PATH / "repo-icon.png")
    window.call('wm', 'iconphoto', window._w, logo) 
    window.mainloop()



def package_file(file_path): 
    if not file_path.endswith('.pkg.tar.zst'):
        raise argparse.ArgumentTypeError('Balíček musí být ve formátu.pkg.tar.zst')
    return file_path



PASSWORD_KEY = 'zlabarch-rep-manager-KEY' #identifikator klice

def create_password():            #vytvoreni administratorskeho hesla pomoci python keyring
    password = getpass.getpass(prompt='Zadejte nové heslo pro admin pravomoce: ')
    confirm_password = getpass.getpass(prompt='Potvrdit heslo: ')
    while password != confirm_password:
        print('Hesla se neschodují, zkuste to znovu.')
        password = getpass.getpass(prompt='Zadejte nové heslo pro admin pravomoce ')
        confirm_password = getpass.getpass(prompt='Potvrdit heslo: ')
    keyring.set_password('system', PASSWORD_KEY, password)
    print(f'Heslo bylo vytvořeno')

def check_admin_password():
    password = keyring.get_password('system', PASSWORD_KEY)
    if not password:
        create_password()
    else:
        input_password = getpass.getpass(prompt='Zadejte admin heslo: ')
        while input_password != password:
            print('Nesprávné heslo, zkuste to znovu')
            input_password = getpass.getpass(prompt='Zadejte admin heslo: ')

def change_password():
    current_password = keyring.get_password('system', PASSWORD_KEY)
    if not current_password:                #pokud heslo neexistuje, tak se zepta uzivatele na nove
        create_password()
    else:
        input_password = getpass.getpass(prompt='Zadejte současné admin heslo: ')
        while input_password != current_password:
            print('Nesprávné heslo, zkuste to znovu')
            input_password = getpass.getpass(prompt='Zadejte současné admin heslo: ')

        new_password = getpass.getpass(prompt='Zadejte nové heslo pro admin pravomoce: ')
        confirm_password = getpass.getpass(prompt='Potvrdit heslo: ')
        while new_password != confirm_password:
            print('Hesla se neschodují, zkuste to znovu.')
            new_password = getpass.getpass(prompt='Zadejte nové heslo pro admin pravomoce ')
            confirm_password = getpass.getpass(prompt='Potvrdit heslo: ')
        
        keyring.set_password('system', PASSWORD_KEY, new_password)
        print(f'Heslo bylo změněno.')



parser = argparse.ArgumentParser()

# admin argument
parser.add_argument('-a', '--admin', action='store_true', help='Zapnutí aplikace s admin pravomocemi')

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


#změna repozitare
changerepodir_parser = subparsers.add_parser('change-repo-dir', help='Změna repozitáře pro balíčky')
changerepodir_parser.add_argument('item', help='Výběr repozitáře, zvolte repozitář ve formátu .db.tar.xz')


change_password_parser = subparsers.add_parser('change-password', help='Změna administrátorského hesla')



args = parser.parse_args()







if args.admin:
    check_admin_password()
    print('admin mode')
else:
    print('user mode')


if args.command == 'add':
    add_pkg(args.package)   
elif args.command == 'del':
    del_pkg(args.item)
elif args.command == 'update':
    print(f'Aktualizováno: {args.item} na {args.new_value}...')
elif args.command =='change-password':
    change_password()
elif args.command =='change-repo-dir':
    print(" ")
else:
    create_gui()