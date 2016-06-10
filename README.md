# Employee lister (a test task for Eastwood lab)

## Installation
Installation instructions are valid for Ubuntu Server 16.04. 
You'll need nginx, uwsgi, PostgreSQL and virtualenv installed on your system. You'll also need development packages (for installing psycopg2):
```
# sudo apt install nginx uwsgi postgresql-9.5 python-virtualenv
# sudo apt install python-dev postgresql-server-dev-9.5
```
Create new virtualenv for application and populate it with needed dependencies:
``` 
$ virtualenv app_env
$ source app_env/bin/activate
$ pip install Django==1.9.7 psycopg2 django-phonenumber-field
```
then, clone the application: ```git clone https://github.com/arisudesu/ew_test```. Next, create database:
```
# sudo -u postgres psql
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
and replace `SECRET_KEY` value with something random.
