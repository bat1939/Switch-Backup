import os
import json
import logging
from datetime import datetime
from netmiko import ConnectHandler
from secrects import switch_user, switch_password

#Loading the device json file and adding to a variable 
device_json = open (os.path.expanduser('~/scripts/switch.json'), 'r')
device_list = json.load(device_json)
device_json.close()

show_run = 'show run'

date = datetime.now().strftime('%Y%m%d')

#Using this variable to compare the number of switches that have been attempted to backup to the number of done devices. 
d = 0 #Setting done count to zero

#Creating the log file
logpath = '~/scripts/logging'
logfile = 'switch_backup.log'
os.makedirs(os.path.expanduser(logpath), exist_ok=True)
logging.basicConfig(
    filename=os.path.join(os.path.expanduser(logpath), logfile),
    level=logging.WARNING,
    format='%(asctime)s:%(levelname)s:%(message)s'
    )

l = open (os.path.join(os.path.expanduser(logpath), logfile), 'a')
l.write('\n' + date + '\n')


#Opening the switch.json file that has all the switch ip information
for switch in device_list['switch_list']:
    #print('Attempting to back up {}'.format(switch['hostname']), end='\r')
    device = {
        'device_type': switch['os'],
        'host': switch['ip_address'],
        'username': switch_user,
        'password': switch_password,
}
#Trying logging into the switch to do a show run and save that to a text file
    try:
        with ConnectHandler(**device) as net_connect:
            no_pager_command = ''
            if switch['os'] == 'brocade_fastiron':
                no_pager_command = 'skip-page-display'
            elif switch['os'] == 'dell_os10':
                no_pager_command = 'terminal length 0'
            if no_pager_command:
                net_connect.send_command(no_pager_command)
            running_config = net_connect.send_command(show_run)
            net_connect.disconnect()
    except:
        l.write('Device {} IP {} has failed the backup \n'.format(switch['hostname'],switch['ip_address']))
        continue

###Create folder and file by hostname###
    hostname_dir = '~/scripts/config_switch/'+switch['hostname']+'/'
    os.makedirs(os.path.expanduser(hostname_dir), exist_ok=True)
    hostname_file = 'running_config_{}.txt'.format(date)
    f = open(os.path.join(os.path.expanduser(hostname_dir), hostname_file), 'w+')
    f.write(running_config)
    f.close()
    d+=1


if (d == len(device_list['switch_list'])):
    l.write('Backups are completed for all devices. \n')
    l.close()
