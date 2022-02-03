1. Build docker: `docker-compose up --build`

?. Migrate: `docker-compose run --rm web python manage.py migrate`

?. Create super user: `docker-compose run --rm web python manage.py createsuperuser`

1. Enter db container: `docker exec -it lims_db_server_postgres bash`

1. cd to backup directory: `cd var/lib/postgresql/backup`

    https://www.postgresql.org/docs/8.0/backup.html

1. Restore from backup: `psql -U sa lims_db < lims_db_backup.tar`

1. Restart container