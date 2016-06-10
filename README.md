# Employee lister (a test task for Eastwood lab)

## Installation
Installation instructions are valid for Ubuntu Server 16.04. 
You'll need nginx, uwsgi, PostgreSQL and virtualenv installed on your system. You'll also need development packages (for installing psycopg2):
```
$ sudo apt install nginx uwsgi uwsgi-plugin-python postgresql-9.5 python-virtualenv
$ sudo apt install python-dev postgresql-server-dev-9.5
```
Create new virtualenv for application and populate it with needed dependencies:
``` 
$ virtualenv app_env
$ source app_env/bin/activate
$ pip install Django==1.9.7 psycopg2 django-phonenumber-field
```
then, clone the application: ```git clone https://github.com/arisudesu/ew_test```. Next, create database:
```
$ sudo -u postgres psql
postgres=# create database your_db;
postgres=# create user your_user with password 'your_password';
postgres=# grant all on database your_db to your_user;
```
configure databases in `ew_test/settings.py` (replace existing data with yours):
```
DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql',
      'NAME': 'your_db',
      'USER': 'your_user',
      'PASSWORD': 'your_password',
      'HOST': 'localhost',
      'PORT': '',
    }
}
```
and replace `SECRET_KEY` value with something random. Then, perform database setup: `python manage.py migrate` and setup static files: `python manage.py collectstatic`. Next, configure uwsgi and nginx:
`/etc/uwsgi/apps-available/ew_test.ini`:
```
[uwsgi]
plugin = python
socket = /run/ew_test.sock
chmod-socket = 660
chown-socket = www-data:www-data
workers = 2

home = /path/to/virtualenv
chdir = /path/to/application
module = ew_test.wsgi
```
`/etc/nginx/sites-available/ew_test.conf`:
```
server {
    listen 80 default;
    server_name your_domain.tld;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/run/ew_test.sock;
    }
    
    location /static/ {
        alias /path/to/aplication/staticfiles/;
    }
}
```
and enable these configs.
```
sudo ln -sf /etc/uwsgi/apps-available/ew_test.ini /etc/uwsgi/apps-enabled/ew_test.ini
sudo rm /etc/nginx/sites/enabled/default
sudo ln -sf /etc/nginx/sites-available/ew_test.conf /etc/nginx/sites-enabled/ew_test.conf
sudo systemctl restart uwsgi nginx
```
