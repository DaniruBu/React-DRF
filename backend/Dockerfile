FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /backend
WORKDIR /backend

RUN apt-get update && apt-get install -y gcc libpq-dev

RUN pip install --upgrade pip && \
    pip install --root-user-action=ignore --no-cache-dir -r requirements.txt

EXPOSE 8000
