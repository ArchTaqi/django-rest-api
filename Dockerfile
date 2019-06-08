# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7-alpine
# run in un buffered mode, which is recommended with python running in docker containers
# doesn't buffer outputs, just prints directly
ENV PYTHONUNBUFFERED 1
# create root directory for our project in the container
RUN mkdir /django-rest-api
# Set the working directory to /code
WORKDIR /django-rest-api
# Copy the current directory contents into the container at /code
ADD . /django-rest-api/
# Install any needed packages specified in requirements.txt
RUN pip install pipenv
RUN pipenv install --dev

RUN adduser -D user
USER user