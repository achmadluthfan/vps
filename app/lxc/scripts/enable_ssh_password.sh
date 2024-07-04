#!/bin/bash

VMID="100"

pct exec ${VMID} -- sh -c '
apt-get update &&
apt-get install -y openssh-server &&
sed -i "s/#PasswordAuthentication yes/PasswordAuthentication yes/" /etc/ssh/sshd_config &&
sed -i "s/#PermitRootLogin prohibit-password/PermitRootLogin yes/" /etc/ssh/sshd_config &&
systemctl restart ssh
'