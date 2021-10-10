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

1. Ensure Docker Desktop has been installed and is actively running.
2. After pulling the repo, change directory to LIMS_IMAGE in the console.
3. Execute `docker-compose up --build` in the console.
4. App will now be running on localhost:8000.
5. To add yourself as a super user to access the Django admin page, attach a shell to the lims_web container and run `python manage.py migrations` then `python manage.py createsuperuser` and follow the prompts.
