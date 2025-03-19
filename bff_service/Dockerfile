# Use an official Ubuntu as a parent image
FROM ubuntu:20.04 AS base

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && \
    apt-get install -y \
    curl \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get upgrade -y
# Add Microsoft SQL Server repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/20.04/mssql-server-2019.list | tee /etc/apt/sources.list.d/mssql-server.list && \
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | tee /etc/apt/sources.list.d/msprod.list

# Install SQL Server and mssql-tools
RUN apt-get update
RUN ACCEPT_EULA=Y apt install -y mssql-tools

#install python & pip
RUN apt-get install -y \
    python3 \
    pip

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000