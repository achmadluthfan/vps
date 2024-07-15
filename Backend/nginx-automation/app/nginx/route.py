from app import app, limiter, response
from flask import request
from app.nginx import controller

@app.route('/api/create', methods=['POST'])
@limiter.limit("10 per minute")
def create():
  try:
    data = request.json
    container_ip = data['container_ip']
    site_name = data['site_name']

    success, message = controller.create_nginx_conf(container_ip=container_ip, site_name=site_name)
    if not success:
      return response.failed(400, message)
    return response.success({
      "message" : "success setting and config nginx"
    })
  except Exception as e:
    print(f"[!] Error route create: {e}")
    return response.failed(500, "Internal Server Error")
