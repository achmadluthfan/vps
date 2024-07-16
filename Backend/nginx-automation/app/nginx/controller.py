from app.nginx import utility

def create_nginx_conf(container_ip: str, site_name: str):
  try:
    success_sd, message_sd = utility.create_sub_domain(site_name=site_name)
    if not success_sd:
      return (False, message_sd)
    print("Success")
    success_nc, message_nc = utility.create_nginx_config(site_name=site_name, container_ip=container_ip)
    if not success_nc:
      return (False, message_nc)
    return (True, None)
  except Exception as e:
    message = f"[!] Error controller create nginx conf: {e}"
    print(message)
    return (False, message)