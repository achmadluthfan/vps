from app import cur
from config import Config
from datetime import datetime

LXC_TABLE = "lxc"
SSH_KEY_TABLE = "ssh_keys"
class LXCDB:
    def __init__(self, vmid, hostname, password, ostemplate, lxc_type):
        self.vmid = vmid
        self.hostname = hostname
        self.password = password
        self.ostemplate = ostemplate
        self.lxc_type = lxc_type
        self.created = datetime.now()
        self.updated = datetime.now()

    def to_dict(self) -> dict:
        return {
            "vmid": self.vmid,
            "hostname": self.hostname,
            "password": self.password,
            "ostemplate" : self.ostemplate,
            "lxc_type": self.lxc_type,
            "created": self.created,
            "updated": self.updated
        }

    def insert_lxc(self):
        try:
            ADD_LXC_QUERY = (
                f"""INSERT INTO {LXC_TABLE} (created, updated, vmid, hostname, password, ostemplate, lxc_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s);"""
            )
            with Config.conn.cursor() as cur:
                cur.execute(ADD_LXC_QUERY, (
                    self.created, self.updated, self.vmid, self.hostname, self.password, self.ostemplate, self.lxc_type
                ))
                Config.conn.commit()
            return True, None
        except Exception as e:
            Config.conn.rollback()
            return False, f"[!] Error adding LXC data: {e}"
    
    @staticmethod
    def get_all_lxc():
        try:
            GET_ALL_LXC_QUERRY = (
                f"""SELECT * FROM {LXC_TABLE};"""
            )
            cur.execute(GET_ALL_LXC_QUERRY)
            rows = cur.fetchall()
            columns = ['vmid', 'created', 'updated', 'hostname', 'password', 'ostemplate', 'lxc_type']
            data = [dict(zip(columns, row)) for row in rows]
            return (True, data)
        except Exception as e:
            return (False, f"[!] Error get all LXC data: {e}")


    @staticmethod
    def delete_lxc(vmid):
        try:
            DELETE_LXC_QUERY = (
                f"""DELETE FROM {LXC_TABLE} WHERE vmid = %s;"""
            )
            cur.execute(DELETE_LXC_QUERY, (vmid,))
            Config.conn.commit()
            return (True, None)
        except Exception as e:
            Config.conn.rollback()
            return (False, f"[!] Error database delete LXC: {e}")
    
    @staticmethod
    def get_all_vmid():
        try:
            ALL_VMID_LXC = (
                f"""SELECT vmid FROM {LXC_TABLE};"""
            )
            cur.execute(ALL_VMID_LXC)
            vmid_data = cur.fetchall()
            vmid_list = [row[0] for row in vmid_data]
            return (True, vmid_list)
        except Exception as e:
            return (False, f"[!] Error database get all vmid LXC: {e}")
    
    @staticmethod
    def insert_ssh_key(vmid:int, key_name: str, private_key: str, public_key: str):
        try:
            INSERT_SSH_KEY = (
                f"""
        INSERT INTO {SSH_KEY_TABLE} (vmid, key_name, private_key, public_key)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (key_name) 
        DO UPDATE SET private_key = EXCLUDED.private_key, public_key = EXCLUDED.public_key;
        """
            )
            cur.execute(INSERT_SSH_KEY, (vmid, key_name, private_key, public_key, ))
            Config.conn.commit()
            return (True, None)
        except Exception as e:
            Config.conn.rollback()
            return (False, f"[!] Error database insert ssh key: {e}")
    
    @staticmethod
    def get_ssh_key(vmid):
        try:
            GET_SSH_KEY = (
                f"""SELECT private_key, key_name FROM {SSH_KEY_TABLE} WHERE vmid = %s"""
            )
            cur.execute(GET_SSH_KEY, (vmid, ))
            result = cur.fetchone()
            private_key = result[0]
            key_name = result[1]
            return (True, (private_key, key_name))
        except Exception as e:
            return (False, f"[!] Error database get all vmid LXC: {e}")
    
    @staticmethod
    def delete_ssh_key(vmid):
        try:
            DELETE_SSH_KEY_QUERY = (
                f"""DELETE FROM {SSH_KEY_TABLE} WHERE vmid = %s;"""
            )
            cur.execute(DELETE_SSH_KEY_QUERY, (vmid,))
            Config.conn.commit()
            return (True, None)
        except Exception as e:
            Config.conn.rollback()
            return (False, f"[!] Error database delete SSH key: {e}")
