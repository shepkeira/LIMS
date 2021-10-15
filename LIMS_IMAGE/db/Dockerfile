FROM mcr.microsoft.com/mssql/server:2019-latest

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=Lab_rats2021
EXPOSE 1433

COPY db_setup.sql /docker-entrypoint-initdb.d/db_setup.sql