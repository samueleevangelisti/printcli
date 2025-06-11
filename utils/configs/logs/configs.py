'''
configs.py
'''
from utils import paths



IS_DEBUG = False
IS_LOG_FILE = False
LOG_FOLDER_PATH = paths.resolve_path(paths.get_folder_path(__file__), '../../../logs/')
