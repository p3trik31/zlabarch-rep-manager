import tkinter
import argparse
import os

# Define command-line arguments
parser = argparse.ArgumentParser()

# Add admin mode argument
parser.add_argument('-a', '--admin', action='store_true', help='Activate admin mode')

# Add command argument and sub-commands
subparsers = parser.add_subparsers(title='commands', dest='command')


# Add "add" sub-command
add_parser = subparsers.add_parser('add', help='Add a new item')
add_parser.add_argument('item', help='Item to add')

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
    print('Welcome to admin mode!')
else:
    print('user mode')

# Perform the requested command
if args.command == 'add':
    print(f'Adding {args.item}...')
elif args.command == 'del':
    print(f'Deleting {args.item}...')
elif args.command == 'update':
    print(f'Updating {args.item} to {args.new_value}...')
#else:
#    print('No command specified. Use -h or --help for help.')
