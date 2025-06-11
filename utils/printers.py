'''
This module is from samueva97.
Do not modify it
'''
from cups import Connection

from utils.configs.printers import configs
from utils import logs
from utils import paths









class Printer:


    def __init__(self, name, description, location):
        self.name = name
        self.description = description
        self.location = location









def list_printers():
    '''
    List all the printers
    
    Returns
    -------
    list<str>

    Raises
    ------
    RuntimeError
    '''
    return [Printer(name, value['printer-info'], value['printer-location']) for name, value in Connection().getPrinters().items()]



def show_default_printer():
    '''
    Return the defautl printer

    Returns
    -------
    str

    Raises
    ------
    RuntimeError
    '''
    return Connection().getDefault()



def print_file(printer, file_path, copies):
    '''
    Print a file using the specified printer

    Parameters
    ----------
    printer : str
        Printer to use
    file_path : str
        Path of the file
    copies : int
        Number of copies

    Raises
    ------
    RuntimeError
    '''
    if not configs.IS_PRINT:
        logs.warning(f"configs.IS_PRINT: {configs.IS_PRINT}, printer: {printer}, file_path: {file_path}, copies: {copies}")
        return
    Connection().printFile(printer, file_path, paths.get_file_name(file_path), {
        'copies': str(copies)
    })
