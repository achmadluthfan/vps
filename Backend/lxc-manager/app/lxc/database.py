from app import cur, config
from datetime import datetime

LXC_TABLE = "lxc"
SSH_KEY_TABLE = "ssh_keys"
class LXCDB:
    def __init__(self, vmid, uuid, hostname, password, ipv4, ostemplate, lxc_type):
        self.vmid = vmid
        self.uuid = uuid
        self.hostname = hostname
        self.password = password
        self.ipv4 = ipv4
        self.ostemplate = ostemplate
        self.lxc_type = lxc_type
        self.created = datetime.now()
        self.updated = datetime.now()

    def to_dict(self) -> dict:
        return {
            "vmid": self.vmid,
            "uuid": self.uuid,
            "hostname": self.hostname,
            "password": self.password,
            "ipv4": self.ipv4,
            "ostemplate" : self.ostemplate,
            "lxc_type": self.lxc_type,
            "created": self.created,
            "updated": self.updated
        }

    def insert_lxc(self):
        try:
            ADD_LXC_QUERY = (
                f"""INSERT INTO {LXC_TABLE} (created, updated, vmid, uuid, hostname, password, ipv4, ostemplate, lxc_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            )
            with config.conn.cursor() as cur:
                cur.execute(ADD_LXC_QUERY, (
                    self.created, self.updated, self.vmid, self.hostname, self.password, self.ostemplate, self.lxc_type
                ))
                config.conn.commit()
            return True, None
        except Exception as e:
            config.conn.rollback()
            return False, f"[!] Error adding LXC data: {e}"
    
    @staticmethod
    def get_all_lxc():
        try:
            GET_ALL_LXC_QUERRY = (
                f"""SELECT * FROM {LXC_TABLE};"""
            )
            cur.execute(GET_ALL_LXC_QUERRY)
            rows = cur.fetchall()
            columns = ['vmid', 'uuid', 'created', 'updated', 'hostname', 'password', 'ipv4', 'ostemplate', 'lxc_type']
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
            config.conn.commit()
            return (True, None)
        except Exception as e:
            config.conn.rollback()
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
            config.conn.commit()
            return (True, None)
        except Exception as e:
            config.conn.rollback()
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
            config.conn.commit()
            return (True, None)
        except Exception as e:
            config.conn.rollback()
            return (False, f"[!] Error database delete SSH key: {e}")
    
    @staticmethod
    def insert_server(vmid:int, site_name: str, port: int, dns_record_id:str):
        try:
            ADD_LXC_QUERY = (
                f"""INSERT INTO server (vmid, site_name, port, dns_record_id)
                VALUES (%s, %s, %s, %s);"""
            )
            with config.conn.cursor() as cur:
                cur.execute(ADD_LXC_QUERY, (
                    vmid, site_name, port, dns_record_id
                ))
                config.conn.commit()
            return True, None
        except Exception as e:
            config.conn.rollback()
            return False, f"[!] Error adding server data: {e}"

    @staticmethod
    def get_server_by_vmid(vmid: int):
        try:
            GET_SERVER_BY_VM_ID_QUERY = (
                """SELECT site_name, port, dns_record_id FROM server WHERE vmid = %s"""
            )
            cur.execute(GET_SERVER_BY_VM_ID_QUERY, (vmid,))
            row = cur.fetchone()
            
            if row:
                columns = ['site_name', 'port', 'dns_record_id']
                data = dict(zip(columns, row))
                return (True, data)
            else:
                return (False, "No record found for the given vmid.")
        except Exception as e:
            return (False, f"[!] Error retrieving server by vmid: {e}")
    
    @staticmethod
    def get_all_site_name():
        try:
            GET_ALL_SITE_NAME_QUERY = "SELECT site_name FROM server"
            cur.execute(GET_ALL_SITE_NAME_QUERY)
            rows = cur.fetchall()
            
            site_names = [row[0] for row in rows]
            return (True, site_names)
        except Exception as e:
            return (False, f"[!] Error retrieving server names: {e}")

    @staticmethod
    def delete_server(vmid):
        try:
            DELETE_SERVER_QUERY = (
                """DELETE FROM server WHERE vmid = %s;"""
            )
            cur.execute(DELETE_SERVER_QUERY, (vmid,))
            config.conn.commit()
            return (True, None)
        except Exception as e:
            config.conn.rollback()
            return (False, f"[!] Error database delete SSH key: {e}")
