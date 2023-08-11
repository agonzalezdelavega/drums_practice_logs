# FROM python3:ubuntu

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV PATH="/scripts:${PATH}"

# RUN pip install --upgrade pip

# COPY ./requirements.txt /requirements.txt

# # RUN apk add --update --no-cache postgresql-client jpeg-dev tesseract-ocr python3 py3-numpy && \
# #     apk add --update --no-cache --virtual .build-deps \
# #     pip3 install --upgrade pip setuptools wheel && \
# #     gcc g++ libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev \
# #     make python3-dev py-numpy-dev
# RUN apt update -y
# RUN pip install -r requirements.txt
# # RUN apk del .build-deps

# RUN mkdir /app
# WORKDIR /app
# COPY ./drums_practice_logs /app

# COPY ./scripts/ /scripts/
# RUN chmod +x /scripts/*

# USER user

# VOLUME /vol/web
# CMD ["entrypoint.sh"]

# Use the official Python 3.10-slim-buster image as the base
FROM python:3.10-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/scripts:${PATH}"

# Set the working directory
COPY ./requirements.txt /requirements.txt

# Install matplotlib dependencies
RUN apt update && apt upgrade -y && \
    apt install -y --no-install-recommends gcc pkg-config libcairo2 libgdk-pixbuf2.0-0 libpango-1.0-0 libxcb-shm0 libxcb-render0 libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

# Install matplotlib and any other required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into the container

RUN mkdir /app
WORKDIR /app
COPY ./drums_practice_logs /app

COPY ./scripts/ /scripts/
RUN chmod +x /scripts/*

USER user

VOLUME /vol/web

# Start your Python application
CMD ["entrypoint.sh"]
