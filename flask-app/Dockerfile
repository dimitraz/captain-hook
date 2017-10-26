FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV STATIC_INDEX 1

RUN pip install boto3 dropbox redis

COPY . /app