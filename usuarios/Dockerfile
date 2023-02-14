# Pull official base image
FROM python:3.9-slim-buster

# Set work directory
WORKDIR /app

# Set enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install pip requirements
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN python -m pip install -r requirements.txt

# Copy Project
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Gunicorn --bind 0.0.0.0:PORT manage:app
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:3000", "src.app:app"]
