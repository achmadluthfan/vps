import requests
import os
import subprocess
import paramiko
from jinja2 import Template
from dotenv import load_dotenv

load_dotenv()

NGINX_SITES_AVAILABLE = "/etc/nginx/sites-available"
NGINX_SITES_ENABLED = "/etc/nginx/sites-enabled"
ROOT_SERVER_NAME = os.getenv('ROOT_SERVER_NAME')

def create_nginx_config(site_name: str, container_ip: str):
    try:
        with open('./app/deploy/templates/nginxtemp.j2', 'r') as file:
            template_content = file.read()

        server_name = f"{site_name}.{ROOT_SERVER_NAME}"
        data = {
            "server_name": server_name,
            "container_ip": container_ip
        }
        j2_template = Template(template_content)
        config_content = j2_template.render(data)

        site_config_path = os.path.join(NGINX_SITES_AVAILABLE, site_name)
        symlink_path = os.path.join(NGINX_SITES_ENABLED, site_name)

        with open(site_config_path, 'w') as config_file:
            config_file.write(config_content)

        if not os.path.exists(symlink_path):
            os.symlink(site_config_path, symlink_path)
        else:
            print(f"[!] Symlink {symlink_path} already exists.")

        return (True, None)
    except FileNotFoundError as e:
        message = f"[!] File not found: {e}"
        print(message)
        return (False, message)
    except PermissionError as e:
        message = f"[!] Permission error: {e}"
        print(message)
        return (False, message)
    except Exception as e:
        message = f"[!] Error creating NGINX config: {e}"
        print(message)
        return (False, message)


def delete_nginx_conf(site_name:str):
    try:
        site_config_path = os.path.join(NGINX_SITES_AVAILABLE, site_name)
        symlink_path = os.path.join(NGINX_SITES_ENABLED, site_name)

        if not os.path.exists(symlink_path):
            return (False, f"[!] Symlink {symlink_path} does not exist.")
        os.remove(symlink_path)

        if not os.path.exists(site_config_path):
            return (False, f"[!] Configuration file {site_config_path} does not exist.")
        os.remove(site_config_path)

        return (True, None)
    except PermissionError as e:
        message = f"[!] Permission error: {e}"
        print(message)
        return (False, message)
    except Exception as e:
        message = f"[!] Error deleting NGINX config: {e}"
        print(message)
        return (False, message)

auth_key = os.getenv('API_KEY')
zone_id = os.getenv('ZONE_ID')
ip_public = os.getenv('IP_PUBLIC')

def create_sub_domain(site_name: str):
    try:
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        headers = {
        "Authorization": f"Bearer {auth_key}",
        "Content-Type": "application/json"
        }

        data = {
            "type": "A",
            "name": f"{site_name}.{ROOT_SERVER_NAME}",
            "content": ip_public,
            "ttl": 3600,
            "proxied": True,
            "comment": f"Created domain for {site_name}",
        }

        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        if response.status_code == 200 and response_data.get("success", False):
            result = response_data.get("result", {})
            dns_record_id = result.get("id")
            print(f"DNS record for {site_name} created successfully.")
            print("Response:", dns_record_id)
            return (True, (dns_record_id, site_name))
        else:
            print(f"Failed to create DNS record for {site_name}.")
            print("Response:", response_data)
            return (False, response_data)
    except requests.exceptions.RequestException as req_err:
        message = f"[!] Request error creating subdomain in Cloudflare: {req_err}"
        print(message)
        return (False, message)
    except Exception as e:
        message = f"[!] Error creating subdomain in Cloudflare: {e}"
        print(message)
        return (False, message)

def generate_port(vmid:int) -> int:
    try:
        port = vmid + 1900
        return port
    except Exception as e:
        return None

def delete_sub_domain(dns_record_id:str):
    try:
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}"
        headers = {
        "Authorization": f"Bearer {auth_key}",
        "Content-Type": "application/json"
        }
        response = requests.delete(url=url, headers=headers)

        if response.status_code == 200:
            print(f"Successfully delete DNS record id: {dns_record_id}")
            return (True, None)
        else:
            print(f"Failed to delete DNS record id {dns_record_id}.")
            print("Response:", response.json())
            return (False, response.json())
    except Exception as e:
        message = f"[!] Error delete sub domain in Cloudflare: {e}"
        print(message)
        return (False, message)

def ssh_connection(command: str):
    hostname = "host.docker.internal"
    port = 22
    username = "xcode"
    try:
        private_key = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname, port, username, pkey=private_key)
        _, _, stderr = ssh.exec_command(command)

        error_message = stderr.read().decode()
        if error_message:
            return (False, error_message)
    
        return (True, None)
    except Exception as e:
        return (False, str(e))
    finally:
        ssh.close()
