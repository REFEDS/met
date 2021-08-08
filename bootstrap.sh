#!/usr/bin/env bash

# This script run under sudo by default so no need to
# put sudo statements here.
export DEBIAN_FRONTEND=noninteractive

apt-get update

# Avoid annoying Grub prompt
# See https://askubuntu.com/questions/146921/how-do-i-apt-get-y-dist-upgrade-without-a-grub-config-prompt
apt-get -y -o DPkg::options::="--force-confdef" -o DPkg::options::="--force-confold" upgrade

apt-get -y install libpq-dev libxml2-dev libxslt-dev
apt-get -y install libffi-dev libssl-dev
apt-get -y install libjpeg-dev
apt-get -y install gettext
apt-get -y install memcached
apt-get -y install python3
apt-get -y install libmysqlclient-dev
apt-get -y install mysql-server mysql-client
apt-get -y install python3-mysqldb
apt-get -y install python3-virtualenv
apt-get -y install python3-pip

mysql -uroot -e "CREATE USER 'met'@'localhost' IDENTIFIED BY 'met';"
mysql -uroot -e "CREATE DATABASE met;"
mysql -uroot -e "GRANT ALL ON *.* TO 'met'@'localhost';"

# update mysql conf file to allow remote access to the db
sudo sed -i "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf

service mysql restart

echo "export LC_ALL='en_US.UTF-8'" >> /home/vagrant/.profile
echo "export LC_CTYPE='en_US.UTF-8'" >> /home/vagrant/.profile
echo "cd /vagrant/" >> /home/vagrant/.profile
echo "source ~/venvs/met/bin/activate" >> /home/vagrant/.profile

su vagrant << EOF
virtualenv --python=python3 ~/venvs/met
source ~/venvs/met/bin/activate
cd /vagrant
pip install -r requirements.txt
EOF
