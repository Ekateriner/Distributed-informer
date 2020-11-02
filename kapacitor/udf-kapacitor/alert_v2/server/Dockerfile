FROM python:3.8-alpine

RUN yes | pip3 install \
        protobuf\
        https://dl.influxdata.com/kapacitor/releases/python-kapacitor_udf-1.5.4.tar.gz\
        flask\
        requests

ADD ./script.py /

USER root

RUN apk add curl

CMD ["python3", "script.py"]
