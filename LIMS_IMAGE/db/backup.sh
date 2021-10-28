docker exec -it lims_db_server "rm /var/opt/mssql/backup/lims_db_init.bak"
docker exec -it lims_db_server /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'Lab_rats2021' -Q "BACKUP DATABASE [lims_db] TO DISK = N'/var/opt/mssql/backup/lims_db_init.bak' WITH NOFORMAT, NOINIT, NAME = 'lims_db', SKIP, NOREWIND, NOUNLOAD, STATS = 10"
docker cp lims_db_server:/var/opt/mssql/backup/lims_db_init.bak data