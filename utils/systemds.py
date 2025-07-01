'''
This module is from samueva97.
Do not modify it
'''
from utils import prints
from utils import commands



def status(*service_list):
    '''
    Prints services status
    '''
    for service in service_list:
        output_list = commands.run(f"systemctl status {service}", False).split('\n')
        print(output_list[0])
        for line in [line for line in output_list[1:] if 'Active:' in line]:
            if 'active (running)' in line:
                prints.green(line)
            elif 'inactive (dead)' in line:
                prints.red(line)
            else:
                prints.yellow(line)



def is_active(service):
    '''
    Return True if the service is active

    Parameters
    ----------
    service : str
        Requested service

    Returns
    -------
    bool
    '''
    for line in commands.run(f"systemctl status {service}", False).split('\n'):
        if 'Active: active (running)' in line:
            return True



def start(*service_list):
    '''
    Starts services
    '''
    for service in [service for service in service_list if '.service' in service]:
        commands.run(f"sudo systemctl start {service}", True)
    status(*service_list)



def stop(*service_list):
    '''
    Stops services
    '''
    for socket in [service for service in service_list if '.socket' in service]:
        commands.run(f"sudo systemctl stop {socket}", True)
    for service in [service for service in service_list if '.service' in service]:
        commands.run(f"sudo systemctl stop {service}", True)
    status(*service_list)
