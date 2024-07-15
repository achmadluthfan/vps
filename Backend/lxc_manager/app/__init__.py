from flask import Flask
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

cur = Config.conn.cursor()

from app.lxc.routes import proxmox_bp
app.register_blueprint(proxmox_bp, url_prefix='/proxmox/lxc')
