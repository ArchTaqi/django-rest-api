# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7-alpine
# run in un buffered mode, which is recommended with python running in docker containers
# doesn't buffer outputs, just prints directly
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /django_pet_store_service

# Set the working directory to /music_service
WORKDIR /django_pet_store_service

# Copy the current directory contents into the container at /music_service
ADD .. /django_pet_store_service/

# Install any needed packages specified in requirements.txt
RUN pipenv install --dev
