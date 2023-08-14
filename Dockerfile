FROM python:3.10-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt

RUN apt update && apt upgrade -y && \
    apt install -y --no-install-recommends gcc pkg-config libcairo2 libgdk-pixbuf2.0-0 libpango-1.0-0 libxcb-shm0 libxcb-render0 libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./drums_practice_logs /app

COPY ./scripts/ /scripts/
RUN chmod +x /scripts/*

RUN adduser --system --no-create-home --disabled-login django_drums_practice_logs
RUN chown -R django_drums_practice_logs .
USER django_drums_practice_logs

CMD ["entrypoint.sh"]
