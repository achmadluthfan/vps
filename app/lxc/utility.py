from proxmoxer import ProxmoxAPI
from .database import LXCDB

# Connect to the Proxmox API
proxmox = ProxmoxAPI('192.168.1.121', user='root@pam', password='xcode', verify_ssl=False)
node = 'xcode'
ostemplate = {
    "ubuntu-22.04-standard" : "local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst"
}

def create_lxc(container_params: dict):
    try:
        proxmox.nodes(node).lxc.create(**container_params)
        # print(f"[*] LXC container with VM ID {container_params['vmid']} has been created successfully.")
        return (True, None)
    except Exception as e:
        message = f"[!] Util create lxc error: {e}"
        return (False, message)

def start_lxc(vmid: int):
    try:
        proxmox.nodes(node).lxc(vmid).status.start.post()
        # print(f"[*] LXC container with VM ID {vmid} has been started.")
        return (True, None)
    except Exception as e:
        message = f"[!] Util start lxc error: {e}"
        return (False, message)

def interfaces_lxc(vmid):
    try:
        interfaces_info = proxmox.nodes(node).lxc(vmid).interfaces.get()
        return (True, interfaces_info)
    except Exception as e:
        message = f"[!] Util interfaces lxc error: {e}"
        return (False, message)

def shutdown_lxc(vmid):
    try:
        proxmox.nodes(node).lxc(vmid).status.shutdown.post()
        return (True, None)
    except Exception as e:
        message = f"[!] Util shutdown lxc error: {e}"
        return (False, message)

def destroy_lxc():
    pass

def generate_vmid() -> int:
    vmid = None
    success, dorm = LXCDB.get_all_vmid()
    if not success:
        message = dorm
        return (False, message)
    vmid_arr = dorm
    if vmid_arr == []:
        vmid = 100
        return vmid
    
    minimum = min(vmid_arr)
    maximum = max(vmid_arr)
    for i in range(minimum, maximum):
        if i not in vmid_arr:
            vmid = i
            return vmid
    
    vmid = maximum + 1
    return vmid
