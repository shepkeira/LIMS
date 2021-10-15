FROM postgres:latest
ENV POSTGRES_PASSWORD=Messy
ENV POSTGRES_USER=lims-user
ENV POSTGRES_DB=lims-postgres
COPY create_fixtures.sql /docker-entrypoint-initdb.d/create_fixtures.sql