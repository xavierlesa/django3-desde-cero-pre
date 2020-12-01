# Pull base image
FROM python:3.7-alpine

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install core-dependencies dev libs, psycopg2 dependencies
RUN apk --update add \
    build-base \
    # gcc make python3-dev musl-dev libffi-dev \
    postgresql-dev \
    libpq \
    # pillow
    zlib-dev \
    jpeg-dev
    # libjpeg-turbo-dev
    # freetype-dev

# Set work directory
RUN mkdir /code
WORKDIR /code

# install python dependencies
ADD requirements.txt .

# update pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
