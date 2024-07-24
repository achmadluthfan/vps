import os
import psycopg2
import time
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    def __init__(self):
        self.conn = self.wait_for_postgres()
        self.proxmox_host = os.getenv("PROXMOX_HOST")
        self.proxmox_username = os.getenv("PROXMOX_USERNAME")
        self.proxmox_password = os.getenv("PROXMOX_PASSWORD")
        self.proxmox_node = os.getenv("PROXMOX_NODE")
        self.deploy_automation_url = os.getenv("DEPLOY_AUTOMATION_URL")
        self.container_ip_range = os.getenv("CONTAINER_IP_RANGE")
        self.container_gateway = os.getenv("CONTAINER_GATEWAY")
        
        print("[*] Initialize proxmox variable")

    def wait_for_postgres(self):
        max_attempts = 10
        attempt = 0
        while attempt < max_attempts:
            try:
                conn = psycopg2.connect(
                    host=os.getenv("POSTGRES_HOST"),
                    port=os.getenv("POSTGRES_PORT"),
                    dbname=os.getenv("POSTGRES_DB"),
                    user=os.getenv("POSTGRES_USERNAME"),
                    password=os.getenv("POSTGRES_PASSWORD")
                )
                print("[*] Database connected")
                return conn  # Return the connection if successful
            except (Exception, psycopg2.DatabaseError) as e:
                attempt += 1
                print(f"[!] Database Error: {e}. Attempt {attempt}/{max_attempts}")
                time.sleep(5)  # Wait for 5 seconds before retrying
        
        raise Exception("Failed to connect to PostgreSQL after several attempts")

config = Config()