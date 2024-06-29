from proxmoxer import ProxmoxAPI
import time
import json

# Connect to the Proxmox API
proxmox = ProxmoxAPI('192.168.1.121', user='root@pam', password='xcode', verify_ssl=False)
node = 'xcode'
ostemplate = {
    "ubuntu-22.04-standard" : "local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst"
}

def create_lxc(container_params: dict):
    try:
        proxmox.nodes(node).lxc.create(**container_params)
        print(f"LXC container with VM ID {container_params['vmid']} has been created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def start_lxc(vmid: int):
    try:
        proxmox.nodes(node).lxc(vmid).status.start.post()
        print(f"LXC container with VM ID {vmid} has been started.")
    except Exception as e:
        print(f"An error occurred: {e}")

def interface_lxc(vmid):
    try:
        interfaces_info = proxmox.nodes(node).lxc(vmid).interfaces.get()
        return interfaces_info
    except Exception as e:
        print(f"An error occurred: {e}")

def destroy_lxc():
    pass
