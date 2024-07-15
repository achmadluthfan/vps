import utility

def create_nginx_conf(container_ip: str, site_name: str):
  try:
    success_sd = utility.create_sub_domain(site_name=site_name)
    if not success_sd:
      return False
    success_nc = utility.create_nginx_config(site_name=site_name, container_ip=container_ip)
    if not success_nc:
      return False
    return True
  except Exception as e:
    print(f"[!] Error controller create nginx conf: {e}")
    return False