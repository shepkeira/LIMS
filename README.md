# LIMS

Repository for UBC Capstone project 2021/2022, group LIMS 0

- [Introduction](#introduction)
- [Developer Instructions](#developer-instructions)
  - [Set Up Env File](#setting-up-you-env-file)
  - [Creating Super Users](#creating-new-superusers)
  - [Accessing Admin Site](#accessing-the-admin-site)
  - [Making Migrations](#making-migrations)
  - [Testing](#testing)
- [Database Instructions](#database-instructions)
  - [Using Docker Image to Run Web Server](#using-docker-image-to-run-web-server)
  - [Enter the Docker Image](#enter-the-docker-image)
  - [Exporting a Database Backup](#exporting-a-database-backup)
- [Style Guide](LIMS%20Style%20Guide.pdf)
- [Meeting Notes](Notes/)

## Introduction

### Organization Background

A Laboratory Information Management System (LIMS) is an internal software program with multiple modules that manages laboratory work flows and information including but not limited to samples and test orders and results. The implementation of the LIMS will simplify data consolidation, improve data quality and security, facilitate receiving samples and track work orders.

### Description

The client’s target is to prepare a user-friendly LIMS which will have all the options a lab could imagine with different module systems. It should be a plug and play software based integrated LIMS to minimize a requirement of software engineer in a lab facility.

Goals of the LIMS is to develop and deploy a server/cloud-based system that provides effective and efficient management of laboratory work flow and information within the organization. The LIMS will be a proponent part of all the regulatory requirement as it will track personnel activates, monitor equipment, record methods validation, record instrument calibration, record and produce technical documents, integrate measurements of uncertainty, ensure validity of results, general reporting, control data and information management.

### General Objectives:

- To implement a server/cloud-based LIMS to manage various lab work flow and information pertaining to tracking sample from receipt to completion.
- To provide Inventory Management for consumables.
- Maintain track-record of reagents, samples and current location.
- Equipment integration for free-flowing data management, compliant to International Standardized Organization.
- To record Quality Control procedures and meet objectives.
- To facilitate real time reporting and record keeping.
- To use unique identifiers (QR/Barcode).
- To use app enabled devices for easy accessibility.
- Incorporating accounting management to make it a complete package.
- Easy to operate module system for any laboratory persons.
- Clients’ portal to access test results and invoices

More Info in [LIMS.pdf](LIMS.pdf)

## Developer Instructions

### Setting Up You .env File

1. Place your .env file under LIMS_IMAGE
1. Your .env file should be formatted like so

```
SECRET_KEY=fake_key
DJANGO_SETTINGS_MODULE=src.settings

MSSQL_HOST=fake_mssql_host_name
DB_USER=fake_user
DB_PASSWORD=fake_password

POSTGRES_DB=fake_postgres_db_name
POSTGRES_HOST=fake_postgres_host_name
POSTGRES_USER=fake_user
POSTGRES_PASSWORD=fake_password
```

1. For the SECRET_KEY, start up the web server (instructions below) use the bash command to get inside the contianer and run
1. Replace the fake data with the correct data for the rest of the variables.


```
python -c "import secrets; print(secrets.token_urlsafe())"
```

This will generate your own SECRET_KEY

### Creating new superusers

1. `sudo docker exec -it lims_web_server python manage.py migrate`
1. `sudo docker exec -it lims_web_server python manage.py createsuperuser` and follow the prompts.

### Accessing the admin site

1. Get superuser login from [User.md](Users.md)
1. Visit localhost:8000/admin and use the superuser account to login.

Alternatively

1. Get superuser login from [User.md](Users.md)
1. Visit localhost:8000 and login use the superuser account to login
1. In the navigation bar select "Administrator Dashboard" to be redirected to the admin site

### Making migrations

When you change something about the database structure in the application we need to migrate those changes

1. `docker-compose --build`
1. `docker exec -it lims_web_server bash`
1. `python manage.py makemigrations`
1. `python manage.py migrate`

Note: If a change to the models was made that prevents the container from starting before the migrations are made, you can run this command in isolation: `docker-compose run web python manage.py makemigrations` and do the same to migrate.

### Testing

The [testing README](LIMS_IMAGE/web/tests/README.md) is found in the testing folder, along with all the tests

## Docker Instructions

### Using Docker Image to Run Web Server

1. Ensure docker and docker-compose are installed, and that this repo is cloned to your machine.
1. cd into `LIMS_IMAGE`.
1. For first-time setup run `docker-compose up --build db-postgres` to let the database build (make sure you wait until it says the database is ready to accept connections. It may pause after the message 'ok' but that does not mean it is finished).
1. After the database has run bring it down (`CTRL+C`) then run `docker-compose up --build`.

### Enter the Docker Image

1. Start Up the Web Server in one terminal
1. In a new terminal, cd into `LIMS_IMAGE`.
1. Run `docker exec -it lims_db_server_postgres bash`

## Database Instructions

### Exporting a database backup

This is required to persist data from the database in the repository. This will export the data as a backup file that will be used to initialize the database next time the container is built. **When pulling updates with a new database backup, you must rebuild the container.**

To create a database backup, simply run the following command while the container is running: `docker exec -it lims_web_server python manage.py dumpdata -o datadump.json` (this command also assumes the current directory is /LIMS_IMAGE)
