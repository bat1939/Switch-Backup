from netmiko import ConnectHandler
from datetime import datetime
from secrects import switch_user, switch_password
import os
import json


device_list = '/home/vetadmin/scripts/switch.json'
#skip_page_display = "skip-page-display"
#page_display = "page-display"
show_run = "show run"
#show_hostname = "show run | inc hostname"
date = datetime.now().strftime("%Y%m%d")
s = 0
d = 0

#Creating the log file
logpath = ("/home/vetadmin/scripts/logging/")
if not os.path.exists(logpath):
    os.makedirs(logpath)
l= open ("/home/vetadmin/scripts/logging/switch_backup.log", "a")
l.write("\n" + date + "\n")

#Opening the switch.json file that has all the switch ip information
with open(device_list) as json_file:
    data = json.load(json_file)
    for switch in data['switch_list']:
        s+=1
        print("Attempting to back up {}...".format(s), end='\r')
        device = {
            "device_type": switch['os'],
            "host": switch['ip_address'],
            "username": switch_user,
            "password": switch_password,
    }
#Trying logging into the switch to do a show run and save that to a text file
        try:
            with ConnectHandler(**device) as net_connect:
                if switch['os'] == "brocade_fastiron":
                    net_connect.send_command("skip-page-display")
                    running_config = net_connect.send_command(show_run)
                    net_connect.disconnect()
                elif switch['os'] == "dell_os10":
                    net_connect.send_command("terminal length 0")
                    running_config = net_connect.send_command(show_run)
                    net_connect.disconnect()
        except:
            l.write("Device {} IP {} has failed the backup \n".format(switch['hostname'],switch['ip_address']))
            continue

        ###Create folder and file by hostname###
        newpath = ('/home/vetadmin/scripts/config_switch/'+switch['hostname']+'/')
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        f = open("/home/vetadmin/scripts/config_switch/"+switch['hostname']+"/running_config_{}.txt".format(date), "w+")
        f.write(running_config)
        f.close()
        d+=1
        #print(hostname + " Backup Done")

if (d == s):
    l.write("Backups are completed for all devices. \n")
    l.close()
