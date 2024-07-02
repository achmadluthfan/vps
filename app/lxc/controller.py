import json
import time
import os
from app.lxc import utility
from .database import LXCDB

def data():
    try:
      result = []
      
      success, dorm = LXCDB.get_all_lxc()
      if not success:
        message = dorm
        print(message)
        return None
      
      data = dorm
      if data != []:
        for d in data:
          vmid = d['vmid']

          ipv4 = None
          success_interfaces, interfaces_info = utility.interfaces(vmid)
          if not success_interfaces:
            print(f"[!] Interface info error: {e}")
          if interfaces_info != None:
            if 'inet' in interfaces_info[1]:
              ipv4 = interfaces_info[1]["inet"]
          
          success_status, status_info = utility.status(vmid)
          if not success_status:
            print(f"[!] Status info error: {e}")      

          result.append({
            "hostname": d['hostname'],
            "vmid" : vmid,
            "user" : "root",
            "password" : d['password'],
            'ipv4' : ipv4,
            'status' : status_info['status']
          })
      return result

    except Exception as e:
      print(f'Controller data error: {e}')
      return None

def create(lxc_type: str, ostemp: str, hostname: str, password: str):
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

        message = "Successfully create lxc"
        success_create, dorm_create = utility.create(container_params)
        if not success_create:
            message = dorm_create
            print(message)
            return None

        time.sleep(5)
        
        success_start, dorm_start = utility.start(container_params['vmid'])
        if not success_start:
            message = dorm_start

        lxc = LXCDB(
            vmid=container_params['vmid'],
            hostname=container_params['hostname'],
            password=container_params['password'],
            ostemplate=container_params['ostemplate'],
            lxc_type=lxc_type
        )
        success_add, dorm_add = lxc.add_lxc()
        if success_add:
          return {
            'message' : message
        }
        message = dorm_add
        print(message)
        return None
    except Exception as e:
        message = f"[!] Controller error create LXC: {e}"
        print(message)
        return None
    
def start(vmid: int):
    try:
        success, dorm = utility.start(vmid)
        if success == False:
            message = dorm
            print(message)
            return None
        return {
            'message' : 'Start was successful.'
        }
    except Exception as e:
        message = f"[!] Controller error start LXC: {e}"
        print(message)
        return None

def shutdown(vmid: int):
    try:
        success, dorm = utility.shutdown(vmid)
        if success == False:
            message = dorm
            print(message)
            return None
        return {
            'message' : 'Shutdown was successful.'
        }
    except Exception as e:
        message = f"[!] Controller error shutdown LXC: {e}"
        print(message)
        return None

def destroy(vmid: int):
    try:
        success_destroy, dorm_destroy = utility.destroy(vmid)
        if not success_destroy:
            message = dorm_destroy
            print(message)
            return None
        success_delete, dorm_delete = LXCDB.delete_lxc(vmid)
        if not success_delete:
            message = dorm_delete
            print(message)
            return None
        return {
            'message' : 'Destroy was successful.'
        }
    except Exception as e:
        message = f"[!] Controller error destroy LXC: {e}"
        print(message)
        return None
    