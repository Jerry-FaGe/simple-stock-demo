FROM python:3.10-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -U pip \
    && pip install -r requirements.txt \
    && pip cache purge

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
