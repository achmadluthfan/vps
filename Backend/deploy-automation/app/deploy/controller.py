from app.deploy import utility

MANAGE_PORTS_PATH = '/home/xcode/caas/automate/manage_ports.sh'

def deploy_container(container_ip: str, site_name: str, vmid: int):
  try:
    success_csd, message_csd = utility.create_sub_domain(site_name=site_name)
    if not success_csd:
      return (False, message_csd)
    result_csd = message_csd
    dns_record_id = result_csd

    success_cnc, message_cnc = utility.create_nginx_config(site_name=site_name, container_ip=container_ip)
    if not success_cnc:
      return (False, message_cnc)

    command_rn = 'sudo systemctl restart nginx'
    success_rn, message_rn = utility.ssh_connection(command=command_rn)
    if not success_rn:
      return (False, message_rn)
    
    port = utility.generate_port(vmid=vmid)
    if port == None:
      return (False, "Cannot generate port")
    
    command_mp = f"{MANAGE_PORTS_PATH} open {str(port)} {container_ip} 22"
    success_mp, message_mp = utility.ssh_connection(command=command_mp)
    if not success_mp:
      return (False, message_mp)
    
    data = {
      "port": port,
      "dns_record_id": dns_record_id
    }
    return (True, data)
  except Exception as e:
    message = f"[!] Error controller deploy: {e}"
    print(message)
    return (False, message)

def delete_deployed_container(container_ip: str, port:int, site_name:str, dns_record_id:str):
  try:
    command_mp = f"{MANAGE_PORTS_PATH} close {str(port)} {container_ip} 22"
    success_sc, message_sc = utility.ssh_connection(command=command_mp)
    if not success_sc:
      return (False, message_sc)
    
    success_dnc, message_dnc = utility.delete_nginx_conf(site_name=site_name)
    if not success_dnc:
      return (False, message_dnc)
    
    command_rn = 'sudo systemctl restart nginx'
    success_rn, message_rn = utility.ssh_connection(command=command_rn)
    if not success_rn:
      return (False, message_rn)
    
    success_dsd, message_dsd = utility.delete_sub_domain(dns_record_id=dns_record_id)
    if not success_dsd:
      return (False, message_dsd)

    return (True, f"Successfully delete deploy automation")
  except Exception as e:
    message = f"[!] Error controller delete deploy automation: {e}"
    print(message)
    return (False, message)