'''
This module is from samueva97.
Do not modify it
'''
import logging
from logging import StreamHandler
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
import os
import inspect

from utils.configs.logs import configs
from utils import colors
from utils import paths
from utils import datetimes
from utils import converts



_QUERY = logging.DEBUG + 1
_REQUEST = logging.DEBUG + 2
_SUCCESS = logging.INFO + 1









class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    '''
    Timed rotating file handler with correct renaming
    '''



    # pylint: disable-next=unused-argument
    def namer(self, file_name):
        '''
        Overrides
        ---------
        TimedRotatingFileHandler.namer
        '''
        return paths.resolve_path(paths.get_folder_path(self.baseFilename), f"{datetimes.now().isoformat()}-{paths.get_file_name(self.baseFilename)}")



    def rotator(self, source, dest):
        '''
        Overrides
        ---------
        TimedRotatingFileHandler.rotator
        '''
        if paths.is_entry(source):
            os.rename(source, dest)
            with open(dest, 'rb') as source_file:
                with open(f"{dest}.zstd", 'wb') as destination_file:
                    destination_file.write(converts.bytes_to_zstd(source_file.read()))
            os.remove(dest)









class CustomFormatter(Formatter):
    '''
    Formatter for utc time and colored log
    '''
    levelno_color_map = {
        logging.DEBUG: colors.PURPLE,
        _QUERY: colors.ORANGE,
        _REQUEST: colors.BLUE,
        logging.INFO: colors.NONE,
        _SUCCESS: colors.GREEN,
        logging.WARNING: colors.YELLOW,
        logging.ERROR: colors.RED,
        logging.CRITICAL: colors.RED
    }



    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, *, defaults=None):
        '''
        Overrides
        ---------
        Formatter.__init__
        '''
        Formatter.__init__(self, f"{colors.GREY}[%(asctime)s] %(process)d:%(thread)d %(module)s:%(funcName)s{colors.NONE} %(log_color)s(%(levelname)s) %(message)s{colors.NONE}", datefmt, style, validate, defaults=defaults)



    def formatTime(self, record, datefmt=None):
        '''
        Overrides
        ---------
        Formatter.formatTime
        '''
        return datetimes.from_timestamp(record.created).isoformat()



    def formatMessage(self, record):
        '''
        Overrides
        ---------
        Formatter.formatMessage
        '''
        record.message = record.message.replace(colors.NONE, f"{colors.NONE}{CustomFormatter.levelno_color_map[record.levelno]}")
        record.log_color = CustomFormatter.levelno_color_map[record.levelno]
        return Formatter.formatMessage(self, record)









_LOG_RECORD_FACTORY = logging.getLogRecordFactory()



# pylint: disable-next=missing-function-docstring
def custom_log_record_factory(*args, **kwargs):
    record = _LOG_RECORD_FACTORY(*args, **kwargs)
    stack = inspect.stack()[6]
    record.funcName = stack.function
    record.module = str(inspect.getmodulename(stack.filename))
    return record



logging.setLogRecordFactory(custom_log_record_factory)
logging.addLevelName(_QUERY, 'QUERY')
logging.addLevelName(_REQUEST, 'REQUEST')
logging.addLevelName(_SUCCESS, 'SUCCESS')



_LOGGER = logging.getLogger()
_LOGGER.setLevel(logging.DEBUG if configs.IS_DEBUG else logging.INFO)
custom_formatter = CustomFormatter()
console_handler = StreamHandler()
console_handler.setFormatter(custom_formatter)
_LOGGER.addHandler(console_handler)
if configs.IS_LOG_FILE:
    if not paths.is_entry(configs.LOG_FOLDER_PATH):
        os.makedirs(configs.LOG_FOLDER_PATH)
    elif not paths.is_folder(configs.LOG_FOLDER_PATH):
        # pylint: disable-next=broad-exception-raised
        raise Exception(f"`{configs.LOG_FOLDER_PATH}` is not a folder")
    file_handler = CustomTimedRotatingFileHandler(paths.resolve_path(configs.LOG_FOLDER_PATH, 'log.log'), when='midnight')
    file_handler.setFormatter(custom_formatter)
    _LOGGER.addHandler(file_handler)



def debug(text):
    '''
    Print a debug log
    
    Parameters
    ----------
    text : str
        Text of the log
    '''
    logging.debug(text)



def query(text):
    '''
    Print a query log
    
    Parameters
    ----------
    text : str
        Text of the log
    '''
    logging.log(_QUERY, text)



def request(text):
    '''
    Print a request log
    
    Parameters
    ----------
    text : str
        Text of the log
    '''
    logging.log(_REQUEST, text)



def info(text):
    '''
    Print an info log
    
    Parameters
    ----------
    text : str
        Text of the log
    '''
    logging.info(text)



def success(text):
    '''
    Print a success log
    
    Parameters
    ----------
    text : str
        Text of the log
    '''
    logging.log(_SUCCESS, text)



def warning(text):
    '''
    Print a warning log
    
    Parameters
    ----------
    text : str
        Text of the log
    '''
    logging.warning(text)



def error(text):
    '''
    Print an error log
    
    Parameters
    ----------
    text : str
        Text of the log
    '''
    logging.error(text)



def critical(text):
    '''
    Print a critical log
    
    Parameters
    ----------
    text : str
        Text of the log
    '''
    logging.critical(text)



def exception(text):
    '''
    Print an exception log
    
    Parameters
    ----------
    text : str
        Text of the log
    '''
    logging.exception(text)
