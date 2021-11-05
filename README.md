# LIMS

Organization Background
A Laboratory Information Management System (LIMS) is an internal software program with multiple modules that manages laboratory work flows and information including but not limited to samples and test orders and results. The implementation of the LIMS will simplify data consolidation, improve data quality and security, facilitate receiving samples and track work orders.

Description
The client’s target is to prepare a user-friendly LIMS which will have all the options a lab could imagine with different module systems. It should be a plug and play software based integrated LIMS to minimize a requirement of software engineer in a lab facility.

Goals of the LIMS is to develop and deploy a server/cloud-based system that provides effective and efficient management of laboratory work flow and information within the organization. The LIMS will be a proponent part of all the regulatory requirement as it will track personnel activates, monitor equipment, record methods validation, record instrument calibration, record and produce technical documents, integrate measurements of uncertainty, ensure validity of results, general reporting, control data and information management.

General Objectives:

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

More Info in LIMS.pdf

## Instructions

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

### Build and Run Docker Image

1. Ensure docker and docker-compose are installed, and that this repo is cloned to your machine.
1. cd into `LIMS_IMAGE`.
1. Run `docker-compose up --build`.

### Database access from within the container

[Useful link](https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver15&pivots=cs1-bash)

1. Build and run the docker image with the above instructions
2. In a new terminal, enter the docker image with `docker exec -it lims_db_server bash`
3. Connect to the database with `/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "Lab_rats2021"`
4. Use the lims_db database `USE lims_db` and the `go` on a new line
5. If you want to see a list of tables currently in the database, run `SELECT TABLE_NAME FROM information_schema.TABLES`
6. To exit sqlcmd, run `quit`

Modifications to the database here will not be persisted to the repo. To commit database changes to the repo, proceed to the next section.

### Exporting a database backup

1. Ensure the docker container is running.
2. If there is already a backup file in the container, we must delete that first as the backup process will not overwrite any existing files with the same name.
    1. Enter bash in the docker image with `docker exec -it limsimage_db_1 bash`
    2. Delete the existing backup file with `rm /var/opt/mssql/backup/lims_db_init.bak`. There will be no response message if it completed successfully.
        (If you get `no such file` error then the file did not exist, and you are fine to continue)
3. To create a new backup file, from a new terminal (in the LIMS_IMAGE directory) run `docker exec -it limsimage_db_1 /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'Lab_rats2021' -Q "BACKUP DATABASE [lims_db] TO DISK = N'/var/opt/mssql/backup/lims_db_init.bak' WITH NOFORMAT, NOINIT, NAME = 'lims_db', SKIP, NOREWIND, NOUNLOAD, STATS = 10"`
4. Copy the backup file from the container to the host (this will replace the existing backup file in `db/data/`) with `docker cp limsimage_db_1:/var/opt/mssql/backup/lims_db_init.bak LIMS_IMAGE/db/data`

### Creating new superusers and accessing the admin site

1. `sudo docker exec -it lims_web_server python manage.py migrate`
2. `sudo docker exec -it lims_web_server python manage.py createsuperuser` and follow the prompts.
3. Visit localhost:8000/admin (or ngrok tunnel) and use your new superuser account to login.

### Making migrations

1. `docker-compose build`
1. `docker-compose up`
1. `docker exec -t -i [container_id] bash`
1. `python manage.py makemigrations`
1. `python manage.py migrate`
