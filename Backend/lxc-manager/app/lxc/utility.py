from proxmoxer import ProxmoxAPI
from app import config
from .database import LXCDB
import paramiko
import io
import requests
import json

# Proxmox variable
proxmox_host = config.proxmox_host
proxmox_username = config.proxmox_username
proxmox_password = config.proxmox_password
proxmox_node = config.proxmox_node
deploy_automation_url = config.deploy_automation_url
containter_ip_range = config.container_ip_range

proxmox = ProxmoxAPI(host=proxmox_host, user=proxmox_username, password=proxmox_password, verify_ssl=False)
node = 'xcode'
ostemplate = {
    "ubuntu-22.04-standard" : "local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst"
}

def create(container_params: dict):
    try:
        proxmox.nodes(proxmox_node).lxc.create(**container_params)
        return (True, None)
    except Exception as e:
        message = f"[!] Util create lxc error: {e}"
        return (False, message)

def start(vmid: int):
    try:
        proxmox.nodes(proxmox_node).lxc(vmid).status.start.post()
        return (True, None)
    except Exception as e:
        message = f"[!] Util start lxc error: {e}"
        return (False, message)

def interfaces(vmid):
    try:
        interfaces_info = proxmox.nodes(proxmox_node).lxc(vmid).interfaces.get()
        return (True, interfaces_info)
    except Exception as e:
        message = f"[!] Util interfaces lxc error: {e}"
        return (False, message)

def status(vmid):
    try:
        status_info = proxmox.nodes(proxmox_node).lxc(vmid).status.current.get()
        return (True, status_info)
    except Exception as e:
        message = f"[!] Util status lxc error: {e}"
        return (False, message)
    
def shutdown(vmid):
    try:
        proxmox.nodes(proxmox_node).lxc(vmid).status.shutdown.post()
        return (True, None)
    except Exception as e:
        message = f"[!] Util shutdown lxc error: {e}"
        return (False, message)

def destroy(vmid):
    try:
        proxmox.nodes(proxmox_node).lxc(vmid).delete()
        return (True, None)
    except Exception as e:
        message = f"[!] Util destroy lxc error: {e}"
        return (False, message)

def generate_ssh_key():
    try:
        key = paramiko.RSAKey.generate(bits=4096)
        
        private_key_io = io.StringIO()
        key.write_private_key(private_key_io)
        private_key = private_key_io.getvalue()

        public_key_str = f"{key.get_name()} {key.get_base64()}"
        public_key = public_key_str

        return (True, (private_key, public_key))
    except Exception as e:
        message = f"[!] Generate SSH key with paramiko error: {e}"
        return (False, message)

def generate_vmid() -> int:
    try:
        vmid = None
        success, dorm = LXCDB.get_all_vmid()
        if not success:
            message = dorm
            print(message)
            return None
        vmid_arr = dorm
        minimum = 100
        if vmid_arr == []:
            vmid = minimum
            return vmid
        
        maximum = max(vmid_arr)
        for i in range(minimum, maximum):
            if i not in vmid_arr:
                vmid = i
                return vmid
        
        vmid = maximum + 1
        return vmid
    except Exception as e:
        print(f"[!] Error generate vmid: {e}")
        return None

def generate_container_ip(vmid: int) -> str:
    try:
        x = vmid - 100 + 3
        continer_ip = containter_ip_range[:-4] + x
        return continer_ip
    except Exception as e:
        print(f"[!] Error generate container ip: {e}")
        return None

def deploy(site_name: str, container_ip: str, vmid:int):
    try:
        data = {
            "container_ip": container_ip,
            "site_name": site_name,
            "vmid": vmid
        }
        response = requests.post(f"{deploy_automation_url}/api/deploy", data=json.dumps(data))

        if response.status_code != 200:
            response_json = response.json()
            message = response_json['error'].get('message', 'No message provided')
            print(f"Error Message: {message}")
            return (False, message)
        result = response.json()
        data = result['data']
        return (True, data)
    except Exception as e:
        message = f"[!] Hit API nginx conf: {e}"
        return (False, message)

def delete_deployed(dns_record_id:str, container_ip:str, site_name:str, port:int):
    try:
        data = {
            "container_ip": container_ip,
            "site_name": site_name,
            "port": port,
            "dns_record_id": dns_record_id
        }
        response = requests.delete(f"{deploy_automation_url}/api/delete", data=json.dumps(data))

        if response.status_code != 200:
            response_json = response.json()
            message = response_json['error'].get('message', 'No message provided')
            print(f"Error Message: {message}")
            return (False, message)
        return (True, None)
    except Exception as e:
        message = f"[!] Hit API nginx conf: {e}"
        return (False, message)

