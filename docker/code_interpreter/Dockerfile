FROM python:3.11.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY ./code_interpreter/requirements.txt .

RUN pip install --no-cache-dir --no-input -r requirements.txt && pip cache purge

COPY ./code_interpreter .
