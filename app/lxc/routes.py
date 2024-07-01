from flask import Blueprint, request
from app import response
from app.lxc import controller

proxmox_bp = Blueprint('proxmox_bp', __name__)

@proxmox_bp.route('/', methods=['GET'])
def home():
    try:
        result = controller.data_lxc()
        if result == None:
            return response.failed(400, "Something went wrong while fetching data.")
        return response.success(result)
    except Exception:
        return response.failed(500, "Internal server error")

@proxmox_bp.route('/create_lxc', methods=['POST'])
def create_lxc():
    try:
        data = request.get_json()
        if not data:
            return response.failed(400, "Get JSON error")
        lxc_type = data['lxc_type']
        ostemplate = data['ostemplate']
        hostname = data['hostname']
        password = data['password']
        result = controller.create_lxc(
            lxc_type=lxc_type,
            ostemp=ostemplate,
            hostname=hostname,
            password=password
        )
        if result == None:
            return response.failed(400, "No result")
        return response.success(result)
    except Exception:
        return response.failed(500, "Internal server error")

@proxmox_bp.route('/shutdown/<vmid>', methods=['POST'])
def shutdown_lxc(vmid):
    try:
        result = controller.shutdown_lxc(vmid)
        if result == None:
            return response.failed(400, "Shutdown failed.")
        return response.success(result)
    except Exception:
        return response.failed(500, "Internal server error")