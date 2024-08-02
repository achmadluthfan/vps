-- docker-entrypoint-initdb.d/init.sql
-- Additional setup commands

-- Create user table
CREATE TABLE IF NOT EXISTS user (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create lxc table
CREATE TABLE IF NOT EXISTS lxc (
    vmid INTEGER PRIMARY KEY,
    uuid UUID REFERENCES user (uuid) ON DELETE SET NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hostname VARCHAR(255),
    password VARCHAR(255),
    ipv4 VARCHAR(255),
    ostemplate VARCHAR(255),
    lxc_type VARCHAR(255)
);

-- Create ssh_keys table
CREATE TABLE IF NOT EXISTS ssh_keys (
    vmid INTEGER PRIMARY KEY,
    key_name VARCHAR(255) NOT NULL UNIQUE,
    private_key TEXT,
    public_key TEXT,
    CONSTRAINT fk_vmid
        FOREIGN KEY(vmid) 
        REFERENCES lxc(vmid)
        ON DELETE RESTRICT
);

-- Create server table
CREATE TABLE IF NOT EXISTS server (
    vmid INTEGER PRIMARY KEY,
    site_name VARCHAR(255) NOT NULL UNIQUE,
    port INTEGER,
    dns_record_id VARCHAR(255),
    CONSTRAINT fk_vmid
        FOREIGN KEY(vmid) 
        REFERENCES lxc(vmid)
        ON DELETE RESTRICT
);