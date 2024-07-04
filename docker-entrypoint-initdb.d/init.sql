-- docker-entrypoint-initdb.d/init.sql
-- Additional setup commands
CREATE TABLE IF NOT EXISTS lxc (
    vmid INTEGER PRIMARY KEY,
    created TIMESTAMP,
    updated TIMESTAMP,
    hostname VARCHAR(255),
    password VARCHAR(255),
    ostemplate VARCHAR(255),
    lxc_type VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS ssh_keys (
    vmid INTEGER PRIMARY KEY,
    key_name VARCHAR(255) NOT NULL UNIQUE,
    private_key BYTEA,
    public_key BYTEA,
    CONSTRAINT fk_vmid
        FOREIGN KEY(vmid) 
        REFERENCES lxc(vmid)
        ON DELETE RESTRICT
);
