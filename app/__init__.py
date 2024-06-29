from flask import Flask
from proxmox import proxmox_bp

app = Flask(__name__)

app.register_blueprint(proxmox_bp, url_prefix='/proxmox')