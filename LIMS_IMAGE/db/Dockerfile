FROM mcr.microsoft.com/mssql/server:2019-latest

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=Lab_rats2021
EXPOSE 1433

RUN mkdir /var/opt/mssql/backup
COPY /data/lims_db_init.bak /var/opt/mssql/backup/lims_db_init.bak

RUN ( /opt/mssql/bin/sqlservr & ) | grep -q "Service Broker manager has started" \
    && /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P Lab_rats2021 -Q 'RESTORE DATABASE lims_db FROM DISK = "/var/opt/mssql/backup/lims_db_init.bak" WITH MOVE "lims_db" TO "/var/opt/mssql/data/lims_db.mdf"' \
    && pkill sqlservr


CMD ["/opt/mssql/bin/sqlservr"]