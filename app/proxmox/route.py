from flask import request
from proxmox import proxmox_bp
from app import response
from app.proxmox import controller
import util

@proxmox_bp.route('/create_lxc', methods=['POST'])
def create_lxc():
    try:
        data = request.get_json()
        if not data:
            return response.failed(400, "Bad Request")
        lxc_type = data['lxc_type']
        ostemplate = data['ostemplate']
        hostname = data['hostname']
        password = data['password']
        result = controller.create_lxc(
            lxc_type=lxc_type,
            ostemplate=ostemplate,
            hostname=hostname,
            password=password
        )
        if result == None:
            return response.failed(400, "Bad Request")
        return response.success(result)
    except Exception as e:
        return response.failed(400, "Bad Request")

@proxmox_bp.route('/shutdown_lxc', methods=['POST'])
def shutdown_lxc():
    pass