FROM python:latest
ENV PYTHONBUFFEREED=1
WORKDIR /src
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev 
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./ /src/