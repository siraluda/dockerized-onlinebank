# pull from base image
FROM python:3.7-alpine

# set python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN mkdir -p /usr/app
WORKDIR /usr/app/
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system

# Copy web app into working directory
COPY . .