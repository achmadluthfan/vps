from proxmoxer import ProxmoxAPI
from config import Config
from .database import LXCDB
import paramiko
import io

# Proxmox variable
proxmox_host = Config.proxmox_host
proxmox_username = Config.proxmox_username
proxmox_password = Config.proxmox_password
proxmox_node = Config.proxmox_node

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
    vmid = None
    success, dorm = LXCDB.get_all_vmid()
    if not success:
        message = dorm
        return (False, message)
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
