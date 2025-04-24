CREATE DATABASE IF NOT EXISTS frosthand_mariadb;

CREATE USER IF NOT EXISTS 'frosthand_mariadb_user'@'%' IDENTIFIED BY 'frosthand_mariadb_password';

GRANT ALL PRIVILEGES ON frosthand_mariadb.* TO 'frosthand_mariadb_user'@'%';

FLUSH PRIVILEGES;
