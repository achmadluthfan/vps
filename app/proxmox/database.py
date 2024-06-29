from app import cur
from datetime import datetime

class LXC:
    def __init__(self, vmid=0, hostname='', password='', ip_addr='', lxc_type=''):
        self.id = None  # ID will be automatically generated by the database
        self.vmid = vmid
        self.hostname = hostname
        self.password = password
        self.ip_addr = ip_addr
        self.lxc_type = lxc_type
        self.created = datetime.now()
        self.updated = datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "vmid": self.vmid,
            "hostname": self.hostname,
            "password": self.password,
            "ip_addr": self.ip_addr,
            "lxc_type": self.lxc_type,
            "created": self.created,
            "updated": self.updated
        }

    @staticmethod
    def create_table():
        try:
            CREATE_PROXMOX_TABLE = (
                """CREATE TABLE IF NOT EXISTS proxmox (
                    id SERIAL PRIMARY KEY,
                    created TIMESTAMP,
                    updated TIMESTAMP,
                    vmid INTEGER,
                    hostname VARCHAR(255),
                    password VARCHAR(255),
                    ipv4 VARCHAR(255),
                    lxc_type VARCHAR(255)
                );"""
              )
            cur.execute(CREATE_PROXMOX_TABLE)
            return (True, None)
        except Exception as e:
            return (False, f"[!] Error creating table: {e}")

    @staticmethod
    def add_lxc(self):
        try:
            ADD_LXC_QUERY = (
                """INSERT INTO proxmox (created, updated, vmid, hostname, password, ipv4, lxc_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;"""
            )
            cur.execute(ADD_LXC_QUERY, (self.created, self.updated, self.vmid, self.hostname, self.password, self.ip_addr, self.lxc_type))
            self.id = cur.fetchone()[0]
            return (True, None)
        except Exception as e:
            return (False, f"[!] Error add LXC data: {e}")

    @staticmethod
    def get_all_lxc():
        try:
            GET_ALL_LXC_QUERRY = (
                """SELECT * FROM proxmox;"""
            )
            cur.execute(GET_ALL_LXC_QUERRY)
            data = cur.fetchall()
            return (True, data)
        except Exception as e:
            return (False, f"Error get all LXC data: {e}")


    @staticmethod
    def delete_lxc(id):
        try:
            DELETE_LXC_QUERY = (
                """DELETE FROM proxmox WHERE id = %s;"""
            )
            cur.execute(DELETE_LXC_QUERY, (id))
            return (True, None)
        except Exception as e:
            return (False, f"[!] Error delete LXC: {e}")
    
