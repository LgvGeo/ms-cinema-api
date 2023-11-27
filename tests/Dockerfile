FROM python:3.11.6
WORKDIR /opt/tests
ENV PYTHONPATH "${PYTHONPATH}:/opt/"
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
WORKDIR /opt/tests
CMD python utils/wait_for_el.py && python utils/wait_for_redis.py && pytest