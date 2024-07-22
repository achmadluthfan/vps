from flask import Blueprint, request, send_file
from app import response
from app.lxc import controller

proxmox_bp = Blueprint('proxmox_bp', __name__)

@proxmox_bp.route('/', methods=['GET'])
def home():
    try:
        result = controller.data()
        if result == None:
            return response.failed(400, "Something went wrong while fetching data.")
        return response.success(result)
    except Exception:
        return response.failed(500, "Internal server error")

@proxmox_bp.route('/create', methods=['POST'])
def create_lxc():
    try:
        data = request.get_json()
        if not data:
            return response.failed(400, "Get JSON error")
        lxc_type = data['lxc_type']
        ostemplate = data['ostemplate']
        hostname = data['hostname']
        password = data['password']
        result = controller.create(
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
    
@proxmox_bp.route('/start/<vmid>', methods=['POST'])
def start(vmid):
    try:
        result = controller.start(vmid)
        if result == None:
            return response.failed(400, "Start failed.")
        return response.success(result)
    except Exception:
        return response.failed(500, "Internal server error")

@proxmox_bp.route('/shutdown/<vmid>', methods=['POST'])
def shutdown(vmid):
    try:
        result = controller.shutdown(vmid)
        if result == None:
            return response.failed(400, "Shutdown failed.")
        return response.success(result)
    except Exception:
        return response.failed(500, "Internal server error")

@proxmox_bp.route('/destroy', methods=['DELETE'])
def destroy(vmid):
    try:
        data = request.get_json()
        if not data:
            return response.failed(400, "Get JSON error")
        vmid = data['vmid']
        ipv4 = data['ipv4']
        result = controller.destroy(vmid=vmid, ipv4=ipv4)
        if result == None:
            return response.failed(400, "Destroy failed.")
        return response.success(result)
    except Exception:
        return response.failed(500, "Internal server error")

@proxmox_bp.route('/download/key/<vmid>', methods=['GET'])
def download_key(vmid):
    try:
        result = controller.download_key(vmid=vmid)
        if result == None:
            return response.failed(400, "Download key failed.")
        private_key, key_name = result
        print(key_name)
        return send_file(private_key, as_attachment=True, download_name=f"{key_name}_private_key.pem", mimetype="application/x-pem-file")
    except Exception:
        return response.failed(500, "Internal server error")