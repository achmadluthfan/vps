import json
import time
import os
from app.lxc import utility
from app import config
from .database import LXCDB
import io

MAIN_SERVER_NAME = "wehos.online"
MAIN_SERVER_IP = "103.174.114.68"

def data(uuid: str):
    try:
        result = []
        
        success, dorm = LXCDB.get_user_lxc(uuid=uuid)
        if not success:
            message = dorm
            print(message)
            return (False, None)
        
        data = dorm
        if data != []:
            for d in data:
                vmid = d['vmid']

                success_status, status_info = utility.status(vmid)
                if not success_status:
                    print(f"[!] Status info error: {status_info}")    
                
                success_gsbv, dorm_gsbv = LXCDB.get_server_by_vmid(vmid)
                if not success_gsbv:
                    message = dorm_gsbv
                    print(message)
                    return (False, None)
                data_gsbv = dorm_gsbv
                site_name = data_gsbv['site_name']
                website = f"{site_name}.{MAIN_SERVER_NAME}"
                port = data_gsbv['port']

                result.append({
                "vmid" : vmid,
                "user" : "root",
                "password" : d['password'],
                "status" : status_info['status'],
                "server": {
                    "website": website,
                    "port": port,
                    "host": MAIN_SERVER_IP
                }
                })
        return (True, result)

    except Exception as e:
        print(f'Controller data error: {e}')
        return (False, None)

def create(lxc_type: str, ostemp: str, hostname: str, password: str, site_name:str, uuid:str):
    try:
        success_gasn, dorm_gasn = LXCDB.get_all_site_name()
        if not success_gasn:
            return (False, dorm_gasn)
        site_name_list = dorm_gasn
        if site_name in site_name_list:
            return (False, f"Site name already used")

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
            return (False, None)
        private_key, public_key = dorm_key

        vmid = utility.generate_vmid()
        if vmid == None:
            message = f"[!] VMID is None"
            print(message)
            return (False, None)
        
        ipv4 = utility.generate_container_ip(vmid=vmid)
        if ipv4 == None:
            message = f"[!] IPV4 is None: {ipv4}"
            print(message)
            return (False, message)
        gateway = config.container_gateway
        ipv4wmask = ipv4 + config.container_ip_range[-3:]
        
        container_params['vmid'] = vmid
        container_params['ostemplate'] = ostemplate
        container_params['hostname'] = hostname
        container_params['password'] = password
        container_params['ssh-public-keys'] = public_key
        container_params['net0'] = f"name=eth0,bridge=vmbr0,ip={ipv4wmask},gw={gateway}"

        success_create, dorm_create = utility.create(container_params)
        if not success_create:
            message = dorm_create
            print(message)
            return (False, message)

        time.sleep(5)
        
        success_start, dorm_start = utility.start(container_params['vmid'])
        if not success_start:
            message = dorm_start
        
        success_d, dorm_d = utility.deploy(site_name=site_name, container_ip=ipv4, vmid=vmid)
        if not success_d:
            message = dorm_d
            message = f"[!] Error controller deploy: {message}"
            print(message)
            return (False, message)
        data_d = dorm_d
        dns_record_id = data_d['dns_record_id']
        port = data_d['port']

        lxc = LXCDB(
            vmid=container_params['vmid'],
            uuid=uuid,
            hostname=container_params['hostname'],
            password=container_params['password'],
            ostemplate=container_params['ostemplate'],
            lxc_type=lxc_type,
            ipv4=ipv4
        )
        success_il, dorm_il = lxc.insert_lxc()
        if not success_il:
            return (False, f"Failed to insert LXC record: {dorm_il}")

        keyname = f"{container_params['vmid']}_{hostname}"
        success_isk, dorm_isk = LXCDB.insert_ssh_key(vmid=container_params['vmid'], key_name=keyname, private_key=private_key, public_key=public_key)
        if not success_isk:
            return (False, f"Failed to insert SSH key: {dorm_isk}")

        success_is, dorm_is = LXCDB.insert_server(vmid=vmid, site_name=site_name, dns_record_id=dns_record_id, port=port)
        if not success_is:
            return (False, f"Failed to insert server record: {dorm_is}")
        
        return (True, {'message': "Successfully created LXC"})
    except Exception as e:
        message = f"[!] Controller error create LXC: {e}"
        print(message)
        return (False, message)
    
def start(vmid: int):
    try:
        success, dorm = utility.start(vmid)
        if not success:
            message = dorm
            print(message)
            return (False, message)
        data = {
            'message' : 'Start was successful.'
        }
        return (True, data)
    except Exception as e:
        message = f"[!] Controller error start LXC: {e}"
        print(message)
        return (False, None)

def shutdown(vmid: int):
    try:
        success, dorm = utility.shutdown(vmid)
        if not success:
            message = dorm
            print(message)
            return (False, message)
        data = {
            'message' : 'Shutdown was successful.'
        }
        return (True, data)
    except Exception as e:
        message = f"[!] Controller error shutdown LXC: {e}"
        print(message)
        return (False, None)

def destroy(vmid: int):
    try:
        ipv4 = utility.generate_container_ip(vmid=vmid)
        if not ipv4:
            message = "failed to generate ipv4"
            return (False, message)

        success_destroy, dorm_destroy = utility.destroy(vmid)
        if not success_destroy:
            message = dorm_destroy
            print(message)
            return (False, message)
        
        success_delete_key, dorm_delete_key = LXCDB.delete_ssh_key(vmid)
        if not success_delete_key:
            message = dorm_delete_key
            print(message)
            return (False, None)
        
        success_gsbv, dorm_gsbv = LXCDB.get_server_by_vmid(vmid=vmid)
        if not success_gsbv:
            message = dorm_gsbv
            print(message)
            return (False, None)
        data = dorm_gsbv
        site_name = data['site_name']
        port = data['port']
        dns_record_id = data['dns_record_id']

        success_dd, dorm_dd = utility.delete_deployed(dns_record_id=dns_record_id, container_ip=ipv4, site_name=site_name, port=port)
        if not success_dd:
            message = dorm_dd
            print(message)
            return (False, None)
        
        success_ds, dorm_ds = LXCDB.delete_server(vmid=vmid)
        if not success_ds:
            message = dorm_ds
            print(message)
            return (False, None)
        
        success_delete_data, dorm_delete_data = LXCDB.delete_lxc(vmid)
        if not success_delete_data:
            message = dorm_delete_data
            print(message)
            return (False, None)
        
        data = {
            'message' : 'Destroy was successful.'
        }
        return (True, data)
    except Exception as e:
        message = f"[!] Controller error destroy LXC: {e}"
        print(message)
        return (False, None)

def download_key(vmid: int):
    try:
        success, dorm = LXCDB.get_ssh_key(vmid=vmid)
        if not success:
            message = dorm
            print(message)
            return (False, None)
        private_key, key_name = dorm
        private_key_io = io.BytesIO(private_key.encode('utf-8'))
        private_key_io.seek(0) 
        return (True, (private_key_io, key_name))
    except Exception as e:
        message = f"[!] Controller download key LXC: {e}"
        print(message)
        return (False, None)
