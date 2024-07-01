import json
import time
import os
from app.lxc import utility
from .database import LXCDB

def data_lxc():
    try:
      success, dorm = LXCDB.get_all_lxc()
      if success == True:
        data = dorm
        return data
      else:
        message = dorm
        print(message)
        return None
    except Exception as e:
      print(e)
      return None

def create_lxc(lxc_type: str, ostemp: str, hostname: str, password: str):
    try:
        path = os.path.dirname(__file__)
        spec_path = os.path.join(path, 'specification.json')
        with open(spec_path, 'r') as spec:
          specification = json.load(spec)
        container_params = specification.get(lxc_type)

        ostmp_path = os.path.join(path, 'ostemplate.json')
        with open(ostmp_path, 'r') as ot:
          ot_json = json.load(ot)
        ostemplate = ot_json.get(ostemp)
        
        container_params['vmid'] = utility.generate_vmid()
        container_params['ostemplate'] = ostemplate
        container_params['hostname'] = hostname
        container_params['password'] = password

        success_create, dorm_create = utility.create_lxc(container_params)
        if not success_create:
            message = dorm_create
            print(message)
            return None

        time.sleep(5)
        
        success_start, dorm_start = utility.start_lxc(container_params['vmid'])
        if success_start:
            ip_addr = None
            time.sleep(20)
            success_int, dorm_int = utility.interfaces_lxc(container_params['vmid'])
            if success_int:
                interface_lxc = dorm_int
                print(interface_lxc)
                if interface_lxc != None:
                    ip_addr = interface_lxc[1]["inet"]

        else:
            message = dorm_start
            print(message)

        lxc = LXCDB(
            vmid=container_params['vmid'],
            hostname=container_params['hostname'],
            password=container_params['password'],
            ip_addr=ip_addr,
            ostemplate=container_params['ostemplate'],
            lxc_type=lxc_type
        )
        success_add, dorm_add = lxc.add_lxc()
        if success_add:
          return lxc.to_dict()
        else:
          message = dorm_add
          print(message)
          return None
    except Exception as e:
        message = f"[!] Controller error create LXC: {e}"
        print(message)
        return None

def shutdown_lxc(vmid: int):
    success, dorm = utility.shutdown_lxc(vmid)
    if success == False:
        message = dorm
        print(message)
        return None
    return {
        'message' : 'Shutdown was successful.'
    }
    