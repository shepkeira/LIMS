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

More Info in [LIMS.pdf](https://github.com/shepkeira/LIMS/blob/development/LIMS.pdf)

## Developer Instructions
### Setting Up You .env File

1. Place your .env file under LIMS_IMAGE
1. Your .env file should be formatted like so

```
DB_NAME=fake_name
DB_HOST=fake_host
DB_USER=fake_user
DB_PASSWORD=fake_password
SECRET_KEY=fake_key
```

1. Replace the fake data with the correct data for the first 4 variables.
1. For the SECRET_KEY, start up the web server (instructions below) use the bash command to get inside the contianer and run

```
python -c "import secrets; print(secrets.token_urlsafe())"
```

This will generate your own SECRET_KEY

### Creating new superusers

1. `sudo docker exec -it lims_web_server python manage.py migrate`
1. `sudo docker exec -it lims_web_server python manage.py createsuperuser` and follow the prompts.

### Accessing the admin site

1. Get superuser login from [User.md](https://github.com/shepkeira/LIMS/Users.md)
1. Visit localhost:8000/admin and use the superuser account to login.

Alternatively

1. Get superuser login from [User.md](https://github.com/shepkeira/LIMS/blob/development/Users.md)
1. Visit localhost:8000 and login use the superuser account to login
1. In the navigation bar select "Administrator Dashboard" to be redirected to the admin site

### Making migrations

When you change something about the database structure in the application we need to migrate those changes

1. `docker-compose --build`
1. `docker exec -it [web container_id] bash`
1. `python manage.py makemigrations`
1. `python manage.py migrate`

### Testing

The [testing README](https://github.com/shepkeira/LIMS/blob/development/LIMS_IMAGE/web/tests/README.md) is found in the testing folder, along with all the tests

## Docker Instructions

### Using Docker Image to Run Web Server

1. Ensure docker and docker-compose are installed, and that this repo is cloned to your machine.
1. cd into `LIMS_IMAGE`.
1. Run `docker-compose up --build`.

### Enter the Docker Image

1. Start Up the Web Server in one terminal
1. In a new terminal, cd into `LIMS_IMAGE`.
1. Run `docker exec -it lims_db_server bash`

You are now in the docker image

## Database Instructions

### Database access from within the container

[Useful link](https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver15&pivots=cs1-bash)

1. Enter the Docker Image
1. Connect to the database with `/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "Lab_rats2021"`
1. Use the lims_db database `USE lims_db` and the `go` on a new line

If you want to see a list of tables currently in the database, run `SELECT TABLE_NAME FROM information_schema.TABLES`

When you have finished with the database we will exit sqlcmd with the command `quit`

Note: Modifications to the database here will not be persisted to the repo. To commit database changes to the repo, proceed to the next section.

### Exporting a database backup

This is required to persist data from the database in the repository. This will export the data as a backup file that will be used to initialize the database next time the container is built.

#### Method 1: Backup script

While the docker container is running, run the `backup.sh` script in the `db` directory if you're on Unix (Linux/MacOS) or `backup.bat` if you're in Windows. backup.bat also requires you to enter the database password when prompted. In the event this does not work, proceed to method 2.

#### Method 2: Commands

1. Start up the Web Server
1. Remove any exisitng backup files
   1. Enter bash in the docker image with `docker exec -it lims_db_server bash`
   1. Delete the existing backup file with `rm /var/opt/mssql/backup/lims_db_init.bak`.
         >There will be no response message if it completed successfully.
         >If you get `no such file` error then the file did not exist, and you are fine to continue
1. Create new backup file, run `docker exec -it lims_db_server /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'Lab_rats2021' -Q "BACKUP DATABASE [lims_db] TO DISK = N'/var/opt/mssql/backup/lims_db_init.bak' WITH NOFORMAT, NOINIT, NAME = 'lims_db', SKIP, NOREWIND, NOUNLOAD, STATS = 10"`
1. Copy the backup file from the container to the host (replacing the existing backup file in `db/data/`) with `docker cp lims_db_server:/var/opt/mssql/backup/lims_db_init.bak LIMS_IMAGE/db/data`

