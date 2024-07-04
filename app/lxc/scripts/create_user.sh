#!/bin/bash

VMID="__VMID__"
USERNAME="__USERNAME__"
PASSWORD="__PASSWORD__"

pct exec ${VMID} -- useradd ${USERNAME} --create-home --password $(openssl passwd -1 ${PASSWORD}) --gecos ''
pct exec ${VMID} -- usermod -aG sudo ${USERNAME}
pct exec ${VMID} -- sh -c "echo '${USERNAME} ALL=(ALL) ALL' > /etc/sudoers.d/${USERNAME}"
