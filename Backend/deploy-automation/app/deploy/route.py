from app import app, limiter, response
from flask import request
from app.deploy import controller

@app.route('/api/deploy', methods=['POST'])
@limiter.limit("10 per minute")
def deploy():
  try:
    data = request.json
    container_ip = data['container_ip']
    site_name = data['site_name']
    vmid = data['vmid']

    success, message = controller.deploy_container(container_ip=container_ip, site_name=site_name, vmid=vmid)
    if not success:
      return response.failed(400, message)
    result = message
    return response.success(result)
  except Exception as e:
    print(f"[!] Error route create: {e}")
    return response.failed(500, "Internal Server Error")

@app.route('/api/delete', methods=['DELETE'])
@limiter.limit("10 per minute")
def delete():
  try:
    data = request.json
    container_ip = data['container_ip']
    site_name = data['site_name']
    port = data['port']
    dns_record_id = data['dns_record_id']

    success, message = controller.delete_deployed_container(container_ip=container_ip, site_name=site_name, port=port, dns_record_id=dns_record_id)
    if not success:
      return response.failed(400, message)
    return response.success({
      "message" : "success delete deploy automation"
    })
  except Exception as e:
    print(f"[!] Error route create: {e}")
    return response.failed(500, "Internal Server Error")