from functools import wraps
from flask import request, g
from app.lxc.database import LXCDB
from app import response

def own_lxc(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    vmid = request.view_args.get("vmid")
    
    uuid = request.cookies.get("uuid")
    if not uuid:
      return response.failed(401, "Unauthorized!")
    
    succes, message = LXCDB.get_user_vmid(uuid=uuid)
    if not succes:
      return response.failed(404, "Something Wrong in Mid")
    vmid_user_list = message
    
    if vmid not in vmid_user_list:
      return response.failed(401, "Unauthorized!")
    return f(*args, **kwargs)
  decorated_function.__name__ = f.__name__
  return decorated_function
    
def auth_required(f):
  def decorated_function(*args, **kwargs):
    g.uuid = request.cookies.get("uuid")
    if not g.uuid:
      return response.failed(401, "Unauthorized!")
    return f(*args, **kwargs)
  decorated_function.__name__ = f.__name__
  return decorated_function