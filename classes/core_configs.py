'''
core_configs.py
'''
from datetime import datetime

from utils import typechecks
from utils import datetimes



class CoreConfigs:
    '''
    Core configs class
    '''



    def __init__(self, sync_datetime):
        '''
        Parameters
        ----------
        sync_datetime : datetime
            Last sync from repo
        '''
        typechecks.check(sync_datetime, datetime)
        self.sync_datetime = sync_datetime



    @staticmethod
    def from_dict(core_configs_dict):
        '''
        Create core configs from dict

        Parameters
        ----------
        core_configs_dict : dict
            dict from core configs

        Returns
        -------
        CoreConfigs
        '''
        return CoreConfigs(datetimes.from_iso(core_configs_dict['sync_datetime']))



    def to_dict(self):
        '''
        Convert core configs to dict
        
        Returns
        -------
        dict
        '''
        return {
            'sync_datetime': self.sync_datetime.isoformat()
        }
