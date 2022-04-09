# Structure

This repo has the following top level structure
- .github (folder)
- LIMS_IMAGE (folder)
- Notes (folder)
- .gitignore
- LIMS Style Guide.pdf
- LIMS.pdf
- README.md
- Structure.md
- Users.md

## .github
This is a folder that contians our git hub workflows

## .gitignore
This file contians files we want github to ignore when considering differences when merging branches, and commiting code.

## LIMS Style Guide
This file has our initial style guidelines when creating UI changes

## README.md
This file has all of our main README information, such as how to start the program, how to set up etc.

## Structure.md
This is this file. This file contains a discription of what the structure of our reposetory is.

## Users.md
This file has the login information for our temporary users. (This information is not hidden because we do not have any real client data).

## Notes
This folder contains all of our weekly notes from clients, proffessor, and team meetings. Files are named after the date they are taken on DD-MM-YYYY.

## LIMS_IMAGE
This folder contains the project

### db
This folder has all the files related to the database container. 
The backup.bat and backup.sh files are used for creating backups of your current database. 
Dockerfile is used for the creation of our database docker container

#### data
This folder contains our database backup (lims_db_init.bak) which is used to initialize our database data for vizualization purposes. Instructions to create a new backup can be found in the README.md

### db-postgres
This folder has all the files related to the postgres database container.

#### data
This folder contains your locally database storeage. To clear you database and reload the backup, delete all the conents of this folder

### web
This folder has all the files related to our web application container.
Dockerfile and requirements.txt are used for the creation of our web application container.
manage.py is a django file for managing our project, its used in processes such as migrations (instructions for migrations can be found in the README.md).

The project is split into 6 applications (accounts, laboratory, laboratoryorders, orders, and training) each of which is contained in its own folder.

#### Applications
The project is split into 6 applications. Each app is contained within its own folder.
Inside an app there are a few files:
- migrations contains all our migration files, accounting for changes to our database
- __init__.py this file tells our project that this directory should be considered a Python package
- admin.py is used to register your app's models
- apps.py is a configuration file
- models.py has all the models for your application
- urls.py is the URL declarations for this Django app
- views.py where you define the logical method for interacting with models and is used to render different html pages
- baker_recipes.py is used for testing, more information can be found in the README.md in testing

##### accounts
The accounts app is for the user account section of the project. It contains the models for the lab workers, lab admin, and the clients, it also contains the redirect for the correct home page, based on who is logged in.

##### laboratory
The laboratory app is for things specific to a laboratory (equipment, tests, and inventory).

##### orders
The orders app is for the client side or ordering tests, viewing order results, and viewing your history.

##### laboratoryOrders
The laboratoryOrders app is for things that are connected throught the laboratory and orders pages (samples).

##### training
The training app is for things related to lab employee training, such as scheduling, and attendence.

#### src
This is our base project folder, it contains files pertaining to the project as a whole.
- __init__.py this file tells our project that this directoyr should be considered a Python package
- asgi.py using Asynchronous Server Gateway Interface (ASGI) you can use this to deploy your project
- settings.py settings and configuration for this Django project
- urls.py the URL declarations for this Django project
- wsgi.py the entry point for Web Server Gateway Interface (WSGI) compatiable web servers to serve the project

#### templates
The templates folder contains the .html and .css files for our different pages on the site. There are folders for each application, and also a home.html and base.html which are not connected to any one application.
- home.html is our home page for a non-logged in user
- base.html has our navigation bar and all other html pages should extend it

#### tests
This folder contains our testing files, and our testing README

### .env
This file contains our environmental variables. They must be set using the instructions in the README.md

### docker-compose.yml
The docker-compose file is used to build our docker containers
