FROM python:3.11.6
WORKDIR /opt/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
WORKDIR /opt/app/src
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-k", "main.CustomUvicornWorker", "main:app"]