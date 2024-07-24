from flask import Flask
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
config = Config()

CORS(app)

if config.conn is None:
    raise Exception("[!] Failed to connect to the database")

cur = config.conn.cursor()

from app.lxc.routes import lxc_bp
app.register_blueprint(lxc_bp, url_prefix='/proxmox/lxc')

@app.teardown_appcontext
def close_db(error):
    if cur:
        cur.close()
    if Config.conn:
        Config.conn.close()
