# finalProject4AStaggenborg

INF601 - Advanced Programming with Python

Adam Staggenborg

## Description
This project will be using Django to create a website that will have tools to scan IP addresses with NMAP
and perform a traceroute with geolocation data.

Data will be stored in a Sqlite3 database.

## Pip Install Instructions

Please run the following:
```
pip install -r requirements.txt
```

## Other software requirements
You will need to install the latest version of Npcap. This is required for scapy functionality. 
Go here for installation instructions: https://npcap.com

## API Requirements
1. You will need to install the latest version of NMAP.  The installer can be found here: https://nmap.org/download 
2. The NMAP install folder will also need to be added to the system path variable 
3. You will need to signup for a free account to get access to the Geolocation database. 
https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
4. Once you sign up and are able to login, you will need to download a copy of the city database and extract it to the root
of your project.  The database filename should be **GeoLite2-City.mmdb**
5. You will need to register for a free account with API Ninja https://api-ninjas.com
Then you will create a file at the root of the project folder named constants.py with the following contents:
```
API_NINJA_KEY = 'INSERT YOUR API KEY HERE'
```


## Usage
Use the following command in a terminal window to initialize the database:
```
python manage.py makemigrations cyberscan
python manage.py migrate
```

Use the following command in a terminal window to start the web application:
```
python manage.py runserver
```
You will be able to view the web application by browsing to http://127.0.0.1:8000

To create an Admin user use the following command in a terminal window:
```
python manage.py createsuperuser
```

A standard user can be created from the web interface registration page.