# Base python package
FROM python:3.11.3-slim-buster

# Working directory
WORKDIR /app

# Copy the dependencies
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy the files
COPY . .

# Create logs file
RUN touch logs/app_logs.log

EXPOSE 5000

# Executable commands
CMD [ "python3", "app.py"]
