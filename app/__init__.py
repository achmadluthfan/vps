from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

cur = Config.conn.cursor()

from app.lxc.routes import proxmox_bp
app.register_blueprint(proxmox_bp, url_prefix='/proxmox/lxc')
