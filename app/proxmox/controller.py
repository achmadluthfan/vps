import json
import util
import time
from database import LXC

def create_lxc(vmid: int, lxc_type: str, ostemplate: str, hostname: str, password: str):
    try:
        with open('spesification.json', 'r') as spec:
          spesification = json.load(spec)
        container_params = spesification.get(lxc_type)

        with open('ostemplate.json', 'r') as ot:
          ot_json = json.load()
        ostemplate = ot_json.get(ostemplate)
        
        container_params['vmid'] = vmid
        container_params['ostempalte'] = ostemplate
        container_params['hostname'] = hostname
        container_params['password'] = password

        util.create_lxc(container_params)
        util.start_lxc(vmid)

        time.sleep(15)

        interface_lxc = util.interfaces_lxc(vmid)
        ip_addr = interface_lxc[1]["inet"]
        
        lxc = LXC(
            vmid=100,
            hostname=hostname,
            password=password,
            ip_addr=ip_addr,
            lxc_type=lxc_type
        )
        success, dorm = lxc.add_lxc()
        if success == True:
          return lxc.to_dict()
        else:
          message = dorm
          print(message)
          return None
    except Exception as e:
        print(f"[!] Controller error create LXC: {e}")
        return None


    