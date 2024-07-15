import requests
import json
import os
import subprocess
from jinja2 import Environment, FileSystemLoader
from dotenv

load_dotenv()

NGINX_SITES_AVAILABLE = "/etc/nginx/sites-available"
NGINX_SITES_ENABLED = "/etc/nginx/sites-enabled"
TEMPLATES_DIR = "./templates"
ROOT_SERVER_NAME = os.getenv('ROOT_SERVER_NAME')

def create_nginx_config(site_name: str, container_ip: str):
  try:
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template('nginx.j2')

    server_name = f"{site_name}.{ROOT_SERVER_NAME}"
    config_content = template.render(server_name=server_name, container_ip=container_ip)
    site_config_path = os.path.join(NGINX_SITES_AVAILABLE, site_name)

    with open(site_config_path, 'w') as config_file:
      config_file.write(config_content)

    os.symlink(site_config_path, NGINX_SITES_ENABLED)
    
    subprocess.run(['sudo', 'systemctl', 'reload', 'nginx'], check=True)
    return True
  except Exception as e:
    print(f"[!] Error utility create nginx config: {e}")
    return False


auth_email = os.getenv('API_EMAIL')
auth_key = os.getenv('API_KEY')
zone_id = os.getenv('ZONE_ID')
ip_public = os.getenv('IP_PUBLIC')
tags = ["vps:customer"]
url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

def create_sub_domain(site_name: str):
  try:
    headers = {
      "X-Auth-Email": auth_email,
      "X-Auth-Key": auth_key,
      "Content-Type": "application/json"
    }

    data = {
          "type": "A",
          "name": site_name,
          "content": ip_public,
          "ttl": 3600,
          "proxied": True,
          "comment": f"Created domain for {site_name}",
          "tags": tags
      }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print(f"DNS record for {site_name} created successfully.")
        print("Response:", response.json())
        return True
    else:
        print(f"Failed to create DNS record for {site_name}.")
        print("Response:", response.json())
        return False
  except Exception as e:
    print(f"[!] Error create sub domain in Cloudflare: {e}")
    return False