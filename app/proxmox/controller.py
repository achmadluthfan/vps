import json
import util
import time

def create_lxc(vmid: int, lxc_type: str, os: str, hostname: str, password: str):
    with open('spesification.json', 'r') as spec:
      spesification = json.load(spec)
    if lxc_type == 'micro':
      container_params = spesification.get('micro')
    elif lxc_type == 'standard':
      container_params = spesification.get('standard')
    container_params['vmid'] = vmid
    container_params['os'] = os
    container_params['hostname'] = hostname
    container_params['password'] = password

    util.create_lxc(container_params)
    util.start_lxc(vmid)

    time.sleep(15)

    interface_lxc = util.interfaces_lxc(vmid)
    ip_addr = interface_lxc[1]["inet"]
    
    data = {
      'hostname' : hostname,
      'user' : 'root',
      'password' : 'password',
      'ip_addr' : ip_addr
    }
    return data


    