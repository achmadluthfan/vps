import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USERNAME"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        
        print("[*] Database connected")

        proxmox_host = os.getenv("PROXMOX_HOST")
        proxmox_username = os.getenv("PROXMOX_USERNAME")
        proxmox_password = os.getenv("PROXMOX_PASSWORD")
        proxmox_node = os.getenv("PROXMOX_NODE")
        deploy_automation_url = os.getenv("DEPLOY_AUTOMATION_URL")
        container_ip_range = os.getenv("CONTAINER_IP_RANGE")
        container_gateway = os.getenv("CONTAINER_GATEWAY")
        
        print("[*] Initialize proxmox variable")
    except (Exception, psycopg2.DatabaseError) as e:
        conn = None
        print(f"[!] Database Error: {e}")
