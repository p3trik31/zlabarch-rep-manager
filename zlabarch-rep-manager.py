import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import argparse
import os
import getpass
import base64
from pathlib import Path
import keyring


with open('/etc/zlabarch-rep-manager/repo.txt', 'r') as f:          #nacteni souboru repozitare
    REPO_FILE_PATH = f.read().strip()

REPO_FOLDER_PATH = os.path.dirname(REPO_FILE_PATH)                  #cesta k souboru repozitare


UNCHECKED_ACTIONS = '/etc/zlabarch-rep-manager/actions.txt'
ASSETS_PATH = Path(__file__).resolve().parent / "assets" #ikona a pozadi aplikace 


adminmode = False


def add_pkg(path):  # přidání balíčku do repozitare
    try:  # funkce pouziva try a except
        command = ["repo-add", REPO_FILE_PATH, path]
        if adminmode == True:
            subprocess.run(command, check=True)  # použije shell pro vykonání akce skrz subprocess modul
        else:
            with open(UNCHECKED_ACTIONS, 'a') as f:
                f.write(' '.join(command)+ '\n')
    except subprocess.CalledProcessError as err:
        print(f"chyba: {err}")


def del_pkg(package):   #Odebrání balíčku z repozitare
    try:                #funkce pouziva try a except
        command = ["repo-remove", REPO_FILE_PATH, package]
        if adminmode == True:
            subprocess.run(command, check=True)    #použije shell pro vykonání akce skrz subprocess modul 
        else:
            with open(UNCHECKED_ACTIONS, 'a') as f:
                f.write(' '.join(command)+ '\n')
    except subprocess.CalledProcessError as err:
        print(f"chyba: {err}")




def list_pkg_files(path):    #vypis balicku 
    pkg_files = []
    for filename in os.listdir(path):
        if filename.endswith(".pkg.tar.zst"):
            base_filename = os.path.splitext(filename)[0]
            pkg_files.append(base_filename)
    return pkg_files


def list_unchecked_actions(path):  #vypis neschvalenych akci
    with open(path, 'r') as f:
        lines = f.readlines()
    return lines


def select_path():
    global output_path
    filetypes = (("Package files", "*.pkg.tar.zst"), ("All files", "*.*"))
    output_path = tk.filedialog.askopenfilename(filetypes=filetypes)
    add_pkg(output_path)
    create_gui()
    




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
    


    actions = list_unchecked_actions(UNCHECKED_ACTIONS)
    for action in actions:
        unchecked_listbox.insert(tk.END, action)
    
    
    # listbox pro balicky
    packages_label = tk.Label(middle_panel, text="Packages", font=("Helvetica", 12, "bold"), bg="#CFD8DC")
    packages_label.pack(side="left", padx=10, pady=10)
    packages_listbox = tk.Listbox(middle_panel, selectmode="multiple", bg="white", fg="#263238", font=("Helvetica", 12))
    packages_listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    pkg_files = list_pkg_files(REPO_FOLDER_PATH)
    for filename in pkg_files:
        packages_listbox.insert(tk.END, filename)
    
    
    # button panel pro hlavni akce
    button_panel = tk.Frame(window, bg="#263238", height=50)
    button_panel.pack(side="top", fill="x")
    add_button = tk.Button(button_panel, text="Add", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5, bd=0, command=select_path) 
    add_button.pack(side="left", padx=10, pady=10)
    del_button = tk.Button(button_panel, text="Del", font=("Helvetica", 12, "bold"), bg="#FF7043", fg="#263238", padx=10, pady=5, bd=0)
    del_button.pack(side="left", padx=10, pady=10)
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







if args.admin:          #v jakem modu se pusti aplikace
    if os.getuid() != 0:
        print("Aplikace potřebuje root pravomoce pro spuštění")
        exit(1)

     
    check_admin_password()
    adminmode = True
else:
    adminmode = False


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