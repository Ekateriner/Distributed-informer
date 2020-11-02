FROM python:3.8

RUN apt-get -qq update && apt-get -qq install -y \
    python3-pip

RUN yes | pip3 install\
    protobuf\
    https://dl.influxdata.com/kapacitor/releases/python-kapacitor_udf-1.5.4.tar.gz

ADD ./script.py /

CMD ["python3", "script.py"]

