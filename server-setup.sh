#!/bin/bash

# NOTA-OIA: Este script esta pensado partiendo de un ubuntu 18.04
# NOTA-OIA: Se puede cambiar "passpasspass" por el password de base de datos que se quiere utilizar (que sera el mismo que va en /usr/local/etc/cms.conf)


set -euxo pipefail

wget https://github.com/cms-dev/cms/releases/download/v1.4.rc1/v1.4.rc1.tar.gz
tar -xzf v1.4.rc1.tar.gz
cd cms

sudo apt update
sudo apt -y dist-upgrade

# NOTA-OIA: Sacamos pascal de los paquetes.
# Feel free to change OpenJDK packages with your preferred JDK.
sudo apt install -y build-essential openjdk-8-jdk-headless postgresql postgresql-client python3.6 cppreference-doc-en-html cgroup-lite libcap-dev zip

# Only if you are going to use pip/venv to install python dependencies
sudo apt install -y python3.6-dev libpq-dev libcups2-dev libyaml-dev libffi-dev python3-pip

# NOTA: De las optional, elegimos solo algunas. Ver https://cms.readthedocs.io/en/v1.4/Installation.html
# Optional
sudo apt install -y nginx-full python2.7 php7.2-cli php7.2-fpm phppgadmin a2ps

echo Y | sudo python3 prerequisites.py install

pip3 install --upgrade pip
sudo pip3 install -r requirements.txt
sudo python3 setup.py install

sudo su -c '(echo passpasspass; echo passpasspass) | createuser --username=postgres --pwprompt cmsuser' postgres
sudo su -c 'createdb --username=postgres --owner=cmsuser cmsdb' postgres
sudo su -c 'psql --username=postgres --dbname=cmsdb --command="ALTER SCHEMA public OWNER TO cmsuser"' postgres
sudo su -c 'psql --username=postgres --dbname=cmsdb --command="GRANT SELECT ON pg_largeobject TO cmsuser"' postgres



# NOTA-OIA: Es necesario hacer log out para que te incluya en el grupo cmsuser
echo "DONE"
echo "*************"
echo "REMEMBER TO LOG OUT (REQUIRED), THEN EDIT /usr/local/etc/cms.conf, THEN DO cmsInitDB"
