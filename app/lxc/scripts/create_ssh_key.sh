#!/bin/bash

VMID="__VMID__"
HOSTNAME="__HOSTNAME__"
USERNAME="__USERNAME__"
KEY_DIR="/home/${USERNAME}/.ssh"
KEY_PATH="${KEY_DIR}/id_rsa"

pct exec ${VMID} -- mkdir -p ${KEY_DIR}
pct exec ${VMID} -- sh -c "ssh-keygen -t rsa -b 4096 -f '${KEY_PATH}' -N ''"
pct download ${VMID} ${KEY_PATH} /path/to/local/destination/${USERNAME}-${HOSTNAME}