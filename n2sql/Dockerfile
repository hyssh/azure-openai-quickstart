FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade -y 

RUN apt autoremove

RUN rm -rf /var/lib/apt/lists/*

# Install required libraries for Pillow and ODBC driver for SQL Server
RUN apt-get update && apt-get install -y build-essential unixodbc-dev libjpeg-dev zlib1g-dev \
    curl gnupg2 apt-transport-https \
    debconf-utils gnupg2 

# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers and tools
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"
RUN apt-get -y install locales \
    && rm -rf /var/lib/apt/lists/*
    
COPY ./requirements.txt ./

COPY ./src ./app

# RUN pip install --upgrade pip setuptools

RUN pip3 install -r requirements.txt 

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "./app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]