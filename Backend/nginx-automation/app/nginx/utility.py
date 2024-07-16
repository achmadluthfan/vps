import requests
import os
import subprocess
from jinja2 import Template
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

NGINX_SITES_AVAILABLE = "/etc/nginx/sites-available"
NGINX_SITES_ENABLED = "/etc/nginx/sites-enabled"
ROOT_SERVER_NAME = os.getenv('ROOT_SERVER_NAME')

def create_nginx_config(site_name: str, container_ip: str):
    try:
        template_path = Path("/app/app/templates/nginx-template.j2")
        
        if not template_path.exists():
            print(f"[!] Template file not found at: {template_path}")
            return (False, f"Template file not found at: {template_path}")

        template_content = template_path.read_text()

        # Render the template with the given data
        server_name = f"{site_name}.{ROOT_SERVER_NAME}"
        data = {
            "server_name": server_name,
            "container_ip": container_ip
        }
        j2_template = Template(template_content)
        config_content = j2_template.render(data)

        # Paths for the new NGINX config and its symlink
        site_config_path = os.path.join(NGINX_SITES_AVAILABLE, site_name)
        symlink_path = os.path.join(NGINX_SITES_ENABLED, site_name)

        # Write the rendered configuration to the appropriate file
        with open(site_config_path, 'w') as config_file:
            config_file.write(config_content)

        # Create a symbolic link in the sites-enabled directory
        if not os.path.exists(symlink_path):
            os.symlink(site_config_path, symlink_path)
        else:
            print(f"[!] Symlink {symlink_path} already exists.")

        # Reload NGINX to apply the new configuration
        subprocess.run(['sudo', 'systemctl', 'reload', 'nginx'], check=True)
        return (True, None)
    except FileNotFoundError as e:
        message = f"[!] File not found: {e}"
        print(message)
        return (False, message)
    except PermissionError as e:
        message = f"[!] Permission error: {e}"
        print(message)
        return (False, message)
    except subprocess.CalledProcessError as e:
        message = f"[!] Error reloading NGINX: {e}"
        print(message)
        return (False, message)
    except Exception as e:
        message = f"[!] Error creating NGINX config: {e}"
        print(message)
        return (False, message)


auth_key = os.getenv('API_KEY')
zone_id = os.getenv('ZONE_ID')
ip_public = os.getenv('IP_PUBLIC')
url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

def create_sub_domain(site_name: str):
  try:
    headers = {
      "Authorization": f"Bearer {auth_key}",
      "Content-Type": "application/json"
    }

    data = {
          "type": "A",
          "name": site_name,
          "content": ip_public,
          "ttl": 3600,
          "proxied": True,
          "comment": f"Created domain for {site_name}",
      }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"DNS record for {site_name} created successfully.")
        print("Response:", response.json())
        return (True, None)
    else:
        print(f"Failed to create DNS record for {site_name}.")
        print("Response:", response.json())
        return (False, response.json())
  except Exception as e:
    message = f"[!] Error create sub domain in Cloudflare: {e}"
    print(message)
    return (False, message)