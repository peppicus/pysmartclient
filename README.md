# pysmartclient

#*******************************************************************
# LINUX
#
apt-get update
#mySQL: http://help.ubuntu-it.org/9.04/ubuntu/serverguide/it/mysql.html
sudo apt-get install mysql-server
#developer library
sudo apt-get install python-dev libmysqlclient-dev

# if you must install python
#sudo apt-get -y install python-pip
#sudo pip install virtualenv

virtualenv sctest 
source sctest/bin/activate

pip install bottle
pip install beaker # for bottler session
pip install SQLAlchemy # ORM
pip install alembic # manage DB versioning
pip install MySQL-python
pip install pysmartclient


