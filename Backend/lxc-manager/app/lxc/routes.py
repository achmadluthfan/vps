from flask import Blueprint, request, send_file
from app import response
from app.lxc import controller

lxc_bp = Blueprint('lxc_bp', __name__)

@lxc_bp.route('/', methods=['GET'])
def home():
    try:
        success, message = controller.data()
        if not success:
            if message == None:
                return response.failed(400, "Something went wrong while fetching data.")
            return response.failed(400, message)
        return response.success(message)
    except Exception:
        return response.failed(500, "Internal server error")

@lxc_bp.route('/create', methods=['POST'])
def create_lxc():
    try:
        data = request.get_json()
        if not data:
            return response.failed(400, "Get JSON error")
        lxc_type = data['lxc_type']
        ostemplate = data['ostemplate']
        hostname = data['hostname']
        password = data['password']
        site_name = data['site_name']

        if not all([lxc_type, ostemplate, hostname, password, site_name]):
            return response.failed(400, "Missing required parameters")
        
        success, message = controller.create(
            lxc_type=lxc_type,
            ostemp=ostemplate,
            hostname=hostname,
            password=password,
            site_name=site_name
        )
        if not success:
            if message == None:
                return response.failed(400, "Someting Wrong!")
            return response.failed(400, message)
        return response.success(message)
    except Exception:
        return response.failed(500, "Internal server error")
    
@lxc_bp.route('/start/<vmid>', methods=['POST'])
def start(vmid):
    try:
        success, message = controller.start(vmid)
        if not success:
            if message == None:
                return response.failed(400, "Start failed.")
            return response.failed(400, message)
        return response.success(message)
    except Exception:
        return response.failed(500, "Internal server error")

@lxc_bp.route('/shutdown/<vmid>', methods=['POST'])
def shutdown(vmid):
    try:
        success, message = controller.shutdown(vmid)
        if not success:
            if message == None:
                return response.failed(400, "Shutdown failed.")
            return response.failed(400, message)
        return response.success(message)
    except Exception:
        return response.failed(500, "Internal server error")

@lxc_bp.route('/destroy/<vmid>', methods=['DELETE'])
def destroy(vmid):
    try:
        success, message = controller.destroy(vmid=int(vmid))
        if not success:
            if message == None:
                return response.failed(400, "Destroy failed.")
            return response.failed(400, message)
        return response.success(message)
    except Exception:
        return response.failed(500, "Internal server error")

@lxc_bp.route('/download/key/<vmid>', methods=['GET'])
def download_key(vmid):
    try:
        success, message = controller.download_key(vmid=vmid)
        if not success:
            if message == None:
                return response.failed(400, "Download key failed.")
            return response.failed(400, message)
        private_key, key_name = message
        print(key_name)
        return send_file(private_key, as_attachment=True, download_name=f"{key_name}_private_key.pem", mimetype="application/x-pem-file")
    except Exception:
        return response.failed(500, "Internal server error")