from app.deploy import utility

def deploy_container(container_ip: str, site_name: str, vmid: int):
  try:
    success_csd, message_csd = utility.create_sub_domain(site_name=site_name)
    if not success_csd:
      return (False, message_csd)
    result_csd = message_csd
    dns_record_id, name = result_csd
    print("Success")
    success_cnc, message_cnc = utility.create_nginx_config(site_name=site_name, container_ip=container_ip)
    if not success_cnc:
      return (False, message_cnc)
    port = utility.generate_port(vmid=vmid)
    if port == None:
      return (False, "Cannot generate port")
    success_rmp, message_rmp = utility.run_manage_ports(action="open", port=port, container_ip=container_ip, container_port=22)
    if not success_rmp:
      return (False, message_rmp)
    data = {
      "server_name": name,
      "port": port,
      "dns_record_id": dns_record_id
    }
    return (True, data)
  except Exception as e:
    message = f"[!] Error controller create nginx conf: {e}"
    print(message)
    return (False, message)

def delete_deployed_container(container_ip: str, port:int, site_name:str, dns_record_id:str):
  try:
    success_rmp, message_rmp = utility.run_manage_ports(action="close", port=port, container_ip=container_ip, container_port=22)
    if not success_rmp:
      return (False, message_rmp)
    
    success_dnc, message_dnc = utility.delete_nginx_conf(site_name=site_name)
    if not success_dnc:
      return (False, message_dnc)
    
    success_dsd, message_dsd = utility.delete_sub_domain(dns_record_id=dns_record_id)
    if not success_dsd:
      return (False, message_dsd)

    return (True, f"Successfully delete deploy automation")
  except Exception as e:
    message = f"[!] Error controller delete deploy automation: {e}"
    print(message)
    return (False, message)