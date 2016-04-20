# jubilee-hub
jubilee-hub is a simple application developed for fun using the Python flask framework to implement a web server to communicate with wireless sensors.  The hub is designed to be deployed on a Raspberry Pi.

Key features:
- The hub and sensors communicate through a RESTful API.
- Sensor readings and details of registered sensors are stored in a SQL database.
- A simple interface to add, remove and view sensors is implemented using HTML & Javascript (accessed from /sensors).
- Historic readings can be downloaded in .csv format (/reports/<sensor_id>).
- A simple watchdog script monitors sensor readings and logs messages if defined thresholds are breached.

The sensors are implemented using ESP8266 wifi modules.

Instructions to deploy to Raspberry Pi running Apache server.

- Create directory for application in `/var/www/`
```bash
mkdir jubilee-hub-prod/
```

- Copy files from development version
```bash
.../jubilee-hub-prod/app/*
.../jubilee-hub-prod/run.py
.../jubilee-hub-prod/db*.py
.../jubilee-hub-prod/config.py
```

- Install python virtual environment into flask folder in jubilee-hub-prod directory
```bash
$ sudo virtualenv flask
```

- Install Python packages
```bash
	$ sudo flask/bin/pip install flask
	$ sudo flask/bin/pip install Flask-SQLAlchemy
	$ sudo flask/bin/pip install sqlalchemy-migrate
```	

- Check package install
```bash
$ flask/bin/python pip list	
```
	decorator (4.0.9)
	Flask (0.10.1)
	Flask-SQLAlchemy (2.1)
	itsdangerous (0.24)
	Jinja2 (2.8)
	MarkupSafe (0.23)
	pbr (1.8.1)
	pip (8.1.1)
	setuptools (20.3.1)
	six (1.10.0)
	SQLAlchemy (1.0.12)
	sqlalchemy-migrate (0.10.0)
	sqlparse (0.1.19)
	Tempita (0.5.2)
	Werkzeug (0.11.5)
	wheel (0.29.0)
	
- Create database and migrate to latest structure
```bash
  $ sudo ./db_create.py
  $ sudo ./db_migrate.py
```

- Create new user in group www-data (i.e. group of apache user)
```bash
  $ sudo useradd flask
  $ sudo -usermod G www-data flask
```

- Create wsgi script `jubilee-hub.wsgi`
```python
activate_this = '/var/www/jubilee-hub-prod/flask/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys

sys.path.append('/var/www/jubilee-hub-prod')

from run import app as application
```

- Create a new record in the hosts file on the Pi `/etc/hosts` to redirect requests to jubilee-hub.local to localhost
```
127.0.0.1	jubilee-hub.local
```

- Add new virtual host config file  `/etc/apache2/sites-available/jubilee-hub.local.conf`
```
<virtualhost *:80>
		ServerName jubilee-hub.local

		WSGIDaemonProcess jubilee-hub user=flask group=www-data threads=5 home=/var/www/jubilee-hub-prod/
		WSGIScriptAlias / /var/www/jubilee-hub-prod/jubilee-hub.wsgi

		<directory /var/www/jubilee-hub-prod>
			WSGIProcessGroup jubilee-hub
			WSGIApplicationGroup %{GLOBAL}
			WSGIScriptReloading On
			Order deny,allow
			Allow from all
		</directory>
</virtualhost>
```

- Enable virtual host and restart Apache
```bash
  $ sudo a2ensite jubilee-hub.local
  $ sudo service apache2 reload
  $ sudo service apache2 restart
```

- Tweak permissions on app folders and restart
```bash
	$ sudo chown -R flask:www-data jubilee-hub-prod
	$ sudo chmod -R 750 jubilee-hub-prod
```

- Run test script `api-test.sh` on localhost to test API
```bash
./api-test.sh --dev
```

- Add jubilee-hub.local to /etc/hosts file on client computer, pointing to the IP address of the Pi.  Use http://jubilee-hub.local in the client browser.  The server then directs the requests to the appropriate virtual server, based on the host name in the header of the request.

- Run test script `api-test.sh` on client computer to test API
```bash
./api-test.sh --prod
```


