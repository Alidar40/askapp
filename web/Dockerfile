# pull official base image
FROM python:3.9.6-alpine

# install dependencies
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev \
    && apk add jpeg-dev

# set work directory
WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["sh", "/app/entrypoint.sh"]