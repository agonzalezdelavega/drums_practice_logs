FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/scripts:${PATH}"

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .build-deps \
      libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev \
      # Matplotlib and Numpy dependencies
      build-base python3-dev py3-pip freetype-dev libpng-dev openblas-dev \
      # MySQL dependencies
     default-libmysqlclient-dev build-essential libssl-dev pkg-config
RUN pip install --no-cache-dir -r /requirements.txt
RUN apk del .build-deps

RUN mkdir /app
WORKDIR /app
COPY ./drums_practice_logs /app

COPY ./scripts/ /scripts/
RUN chmod +x /scripts/*

USER user

VOLUME /vol/web
CMD ["entrypoint.sh"]