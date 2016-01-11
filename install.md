# Install at CentOS 7

## Download source

~~~bash
yum install -y git
cd /opt/
git clone https://github.com/choonho/pyengine.git
~~~

## Install Packages

~~~bash
yum install -y python-devel python-pip mariadb-server mariadb MySQL-python httpd mod_wsgi
~~~

## PIP package install

~~~bash
pip install django
pip install django-log-request-id
pip install dicttoxml
pip install xmltodict
pip install routes
pip install rsa
pip install pytz
~~~

## Make Log directory

~~~bash
mkdir -p /var/log/pyengine
~~~

## Update Python module path environment
~~~bash
echo "/opt/pyengine" > /usr/lib/python2.7/site-packages/pyengine.pth
~~~

# Update Apache configuration

edit /etc/httpd/conf.d/pyengine.conf

~~~text
<VirtualHost *:80>
    Alias /static/ /opt/pyengine/static/
    <Directory /opt/pyengine/static>
        Require all granted
    </Directory>

    WSGIScriptAlias / /opt/pyengine/pyengine/wsgi.py
    WSGIPassAuthorization On

    <Directory /opt/pyengine/pyengine>
    <Files wsgi.py>
        Require all granted
    </Files>
    </Directory>

    AddDefaultCharset UTF-8

</VirtualHost>
~~~

# Create database

~~~bash
systemctl restart mariadb.service
mysql -uroot -e "create database pyengine character set utf8 collate utf8_general_ci"
~~~

# Update django 

~~~bash
cd /opt/pyengine
python manage.py makemigrations
python manage.py migrate
~~~

# Restart apache

~~~bash
systemctl restart httpd.service
~~~
