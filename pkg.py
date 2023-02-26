import tkinter
import argparse
import os
import getpass
import base64


PASSWORD_FILE_PATH = '/etc/zlabarch-rep-manager/admin_password.txt'

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
    print("gui")
