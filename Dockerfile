FROM python:3.11
COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install django
RUN pip install requests

ENTRYPOINT ["python", "./demotask/manage.py"]
CMD ["runserver", "0.0.0.0:8002"]