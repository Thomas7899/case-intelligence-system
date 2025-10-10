FROM python:3.13-slim
ARG BUILD_REV=0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

COPY . /code

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "palantir_system.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]