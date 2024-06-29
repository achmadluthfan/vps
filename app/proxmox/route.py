from proxmox import proxmox_bp
import util

@proxmox_bp.route('/create_lxc', methods=['POST'])
def create_lxc():
    pass

@proxmox_bp.route('/shutdown_lxc', methods=['POST'])
def shutdown_lxc():
    pass