'''
printcli.py
'''
import sys
import time
import json
import click

from utils import prints
from utils import printers
from utils import paths
from utils import systemds



@click.command()
@click.argument('is-list', type=bool)
@click.argument('printer', type=str)
@click.argument('copies', type=int)
@click.argument('path-list-str', type=str)
def _main(is_list, printer, copies, path_list_str):
    path_list = json.loads(path_list_str)

    if is_list:
        printer_list = printers.list_printers()
        name_len = len('name')
        description_len = len('description')
        name_max_len = max([len(printer.name) for printer in printer_list] + [name_len])
        description_max_len = max([len(printer.description) for printer in printer_list] + [description_len])
        print(f"name{' ' * (name_max_len - name_len)}   description{' ' * (description_max_len - description_len)}   location\n")
        for printer in printer_list:
            print(f"{printer.name}{' ' * (name_max_len - len(printer.name))}   {printer.description}{' ' * (description_max_len - len(printer.description))}   {printer.location}")
        sys.exit(0)

    if not path_list:
        prints.red(f"`path_list` is `{path_list}`")
        sys.exit(1)

    for path in path_list:
        if not paths.is_entry(path):
            prints.red(f"`{path}` not found")
            sys.exit(1)

        if paths.is_folder(path):
            prints.red(f"`{path}` is folder")
            sys.exit(1)

    if not systemds.is_active('cups.service'):
        systemds.start('cups.socket', 'cups.service')

    selected_printer = printer
    if not selected_printer:
        printer_list = printers.list_printers()
        name_len = len('name')
        description_len = len('description')
        name_max_len = max([len(printer.name) for printer in printer_list] + [name_len])
        description_max_len = max([len(printer.description) for printer in printer_list] + [description_len])
        print(f"       name{' ' * (name_max_len - name_len)}   description{' ' * (description_max_len - description_len)}   location\n")
        for index, printer in enumerate(printer_list):
            print(f"[{index + 1:>2d}]   {printer.name}{' ' * (name_max_len - len(printer.name))}   {printer.description}{' ' * (description_max_len - len(printer.description))}   {printer.location}")
        selected_printer = printer_list[int(input('Printer: ')) - 1].name

    for path in path_list:
        printers.print_file(selected_printer, path, copies)

    while printers.is_printing():
        time.sleep(3)

    systemds.stop('cups.socket', 'cups.service')



if __name__ == '__main__':
    # pylint: disable-next=no-value-for-parameter
    _main()
