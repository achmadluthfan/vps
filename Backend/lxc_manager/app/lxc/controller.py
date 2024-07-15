import json
import time
import os
from app.lxc import utility
from .database import LXCDB
import io

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
                if success_interfaces and interfaces_info != None:
                    if 'inet' in interfaces_info[1]:
                        ipv4 = interfaces_info[1]["inet"]

                success_status, status_info = utility.status(vmid)
                if not success_status:
                    print(f"[!] Status info error: {status_info}")      

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

        message = "Successfully create lxc"

        success_key, dorm_key = utility.generate_ssh_key()
        if not success_key:
            message = dorm_key
            print(message)
            return None
        private_key, public_key = dorm_key

        vmid = utility.generate_vmid()
        if vmid == None:
            print(f"[!] VMID is None")
            return None
        
        container_params['vmid'] = vmid
        container_params['ostemplate'] = ostemplate
        container_params['hostname'] = hostname
        container_params['password'] = password
        container_params['ssh-public-keys'] = public_key

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
        success_add, dorm_add = lxc.insert_lxc()
        if success_add:
            keyname = f"{container_params['vmid']}_{hostname}"
            success_key_db, dorm_key_db = LXCDB.insert_ssh_key(vmid=container_params['vmid'], key_name=keyname, private_key=private_key, public_key=public_key)
            if success_key_db:
                return {
            'message' : message
            }
            message = dorm_key_db
            print(message)
            
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
        if not success:
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
        if not success:
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
        success_delete_key, dorm_delete_key = LXCDB.delete_ssh_key(vmid)
        if not success_delete_key:
            message = dorm_delete_key
            print(message)
            return None

        success_delete_data, dorm_delete_data = LXCDB.delete_lxc(vmid)
        if not success_delete_data:
            message = dorm_delete_data
            print(message)
            return None
        return {
            'message' : 'Destroy was successful.'
        }
    except Exception as e:
        message = f"[!] Controller error destroy LXC: {e}"
        print(message)
        return None

def download_key(vmid: int):
    try:
        success, dorm = LXCDB.get_ssh_key(vmid=vmid)
        if not success:
            message = dorm
            print(message)
            return None
        private_key, key_name = dorm
        private_key_io = io.BytesIO(private_key.encode('utf-8'))
        private_key_io.seek(0) 
        return (private_key_io, key_name)
    except Exception as e:
        message = f"[!] Controller download key LXC: {e}"
        print(message)
        return None
