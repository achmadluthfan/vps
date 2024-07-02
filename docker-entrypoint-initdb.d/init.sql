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
