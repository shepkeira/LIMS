# LIMS

## Organization Background

A Laboratory Information Management System (LIMS) is an internal software program with multiple modules that manages laboratory work flows and information including but not limited to samples and test orders and results. The implementation of the LIMS will simplify data consolidation, improve data quality and security, facilitate receiving samples and track work orders.

## Description

The client’s target is to prepare a user-friendly LIMS which will have all the options a lab could imagine with different module systems. It should be a plug and play software based integrated LIMS to minimize a requirement of software engineer in a lab facility.

Goals of the LIMS is to develop and deploy a server/cloud-based system that provides effective and efficient management of laboratory work flow and information within the organization. The LIMS will be a proponent part of all the regulatory requirement as it will track personnel activates, monitor equipment, record methods validation, record instrument calibration, record and produce technical documents, integrate measurements of uncertainty, ensure validity of results, general reporting, control data and information management.

## General Objectives

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

## How to set up the Docker image

1. Ensure docker and docker-compose are installed, and that this repo is cloned to your machine.

1. `cd` into `LIMS_IMAGE`

1. Run `docker-compose up --build`, the sample program should periodically print "The last value inserted is: ..."

### Troubleshooting

1. Delete all docker images (view images with `docker images`, delete with `docker image rm <id>`, delete process dependencies with `docker rm <id>`)

### Running and Accessing Postgres Only

1. Ensure docker is installed and this repo is cloned onto your machine

1. cd into `LIMS_IMAGE/POSTGRES`

1. Build docker image with `docker build .`, and take note of the image ID when it is finished (should say `successfully built <id>`). (I will add an image name to the dockerfile in a future commit)

1. Run the docker image with `docker run --name lims-postgres <id>` (do not close the terminal window at this point)

1. Open a new terminal window, and connect to the running docker image with `docker exec -it lims-postgres bash`

1. Connect to the database with `psql -U lims-user -d lims-postgres`

1. Now we are in! We can query the `test` table, insert values, and create more tables!
