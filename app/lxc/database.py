from app import cur
from config import Config
from datetime import datetime

TABLE_NAME = "lxc"
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

    def add_lxc(self):
        try:
            ADD_LXC_QUERY = (
                f"""INSERT INTO {TABLE_NAME} (created, updated, vmid, hostname, password, ostemplate, lxc_type)
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
                f"""SELECT * FROM {TABLE_NAME};"""
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
                f"""DELETE FROM {TABLE_NAME} WHERE vmid = %s;"""
            )
            cur.execute(DELETE_LXC_QUERY, (vmid,))
            Config.conn.commit()
            return (True, None)
        except Exception as e:
            Config.conn.rollback()
            return (False, f"[!] Error delete LXC: {e}")
    
    @staticmethod
    def get_all_vmid():
        try:
            ALL_VMID_LXC = (
                f"""SELECT vmid FROM {TABLE_NAME};"""
            )
            cur.execute(ALL_VMID_LXC)
            vmid_data = cur.fetchall()
            vmid_list = [row[0] for row in vmid_data]
            return (True, vmid_list)
        except Exception as e:
            return (False, f"[!] Error get all vmid LXC: {e}")
