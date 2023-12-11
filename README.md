# finalProject4AStaggenborg

INF601 - Advanced Programming with Python

Adam Staggenborg

## Description
This project will be using Django to create a website that will have tools to scan IP addresses with NMAP
and perform a visual traceroute to IP addresses.

Data will be stored in a Sqlite3 database.

## Pip Install Instructions

Please run the following:
```
pip install -r requirements.txt
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