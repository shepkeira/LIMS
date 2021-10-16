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
### Build and Run Docker Image

1. Ensure docker and docker-compose are installed, and that this repo is cloned to your machine.
1. cd into `LIMS_IMAGE`.
1. Run `docker-compose up --build`.

### Database access from within the container
[Useful link](https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver15&pivots=cs1-bash)

1. Build and run the docker image with the above instructions
1. In a new terminal, enter the docker image with `docker exec -it limsimage_db_1 bash`
1. Connect to the database with `/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "Lab_rats2021"`
1. Use the lims_db database `USE lims_db` and the `go` on a new line

### Exporting a database backup
1. `sudo docker exec -it limsimage_db_1 /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'Lab_rats2021' -Q "BACKUP DATABASE [lims_db] TO DISK = N'/var/opt/mssql/backup/lims_db_init.bak' WITH NOFORMAT, NOINIT, NAME = 'lims_db', SKIP, NOREWIND, NOUNLOAD, STATS = 10"`
1. Replace the lims_db_init.bak file in the data directory
