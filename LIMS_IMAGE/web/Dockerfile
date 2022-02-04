FROM python:3.7
ENV PYTHONBUFFEREED=1
WORKDIR /src
RUN apt-get update -y
RUN apt-get install zbar-tools -y
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev \
    curl
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install -U matplotlib
# Install ODBC Driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17