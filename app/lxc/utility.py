from proxmoxer import ProxmoxAPI
from .database import LXCDB
import paramiko
import io

# Connect to the Proxmox API
ip_proxmox = '192.168.1.121'
proxmox = ProxmoxAPI(host=ip_proxmox, user='root@pam', password='xcode', verify_ssl=False)
node = 'xcode'
ostemplate = {
    "ubuntu-22.04-standard" : "local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst"
}

def create(container_params: dict):
    try:
        proxmox.nodes(node).lxc.create(**container_params)
        return (True, None)
    except Exception as e:
        message = f"[!] Util create lxc error: {e}"
        return (False, message)

def start(vmid: int):
    try:
        proxmox.nodes(node).lxc(vmid).status.start.post()
        return (True, None)
    except Exception as e:
        message = f"[!] Util start lxc error: {e}"
        return (False, message)

def interfaces(vmid):
    try:
        interfaces_info = proxmox.nodes(node).lxc(vmid).interfaces.get()
        return (True, interfaces_info)
    except Exception as e:
        message = f"[!] Util interfaces lxc error: {e}"
        return (False, message)

def status(vmid):
    try:
        status_info = proxmox.nodes(node).lxc(vmid).status.current.get()
        return (True, status_info)
    except Exception as e:
        message = f"[!] Util status lxc error: {e}"
        return (False, message)
    
def shutdown(vmid):
    try:
        proxmox.nodes(node).lxc(vmid).status.shutdown.post()
        return (True, None)
    except Exception as e:
        message = f"[!] Util shutdown lxc error: {e}"
        return (False, message)

def destroy(vmid):
    try:
        proxmox.nodes(node).lxc(vmid).delete()
        return (True, None)
    except Exception as e:
        message = f"[!] Util destroy lxc error: {e}"
        return (False, message)

def run_command(commands: str):
    try:
        proxmox.nodes(node).execute.post(commands=commands)
        return (True, None)
    except Exception as e:
        message = f"[!] Run command in proxmox CLI error: {e}"
        return (False, message)

def generate_ssh_key(passphrase=None):
    try:
        key = paramiko.RSAKey.generate(4096)

        private_key_io = io.BytesIO()
        key.write_private_key(private_key_io, password=passphrase)
        private_key = private_key_io.getvalue()

        public_key_str = f"{key.get_name()} {key.get_base64()}"
        public_key = public_key_str.encode('utf-8')

        return (True, (private_key, public_key))
    except Exception as e:
        message = f"[!] Generate SSH key with paramiko serror: {e}"
        return (False, message)

def enable_ssh_password(vmid: int):
    try:
        commands = f"""
        pct exec {vmid} -- sh -c "apt-get update && \
        apt-get install -y openssh-server && \
        sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
        sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
        systemctl restart ssh"
        """
        
        success, output = run_command(commands.strip())
        if not success:
            message = f"[!] Error executing command: {output}"
            return (False, message)

        return (True, None)
    except Exception as e:
        message = f"[!] Error in enabling SSH password authentication: {e}"
        return (False, message)

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
