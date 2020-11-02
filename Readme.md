# Distributed events informer

This part of project

### Remark:

Please, read all Readme files before runing (in all subdirectories)

You can use this code partly

## Getting Started

Run docker-compose file

### Prerequisites

You need to install kapacitor, telegraf (collector) and influxdb (storage). Please, use docker pull.

And run them:

```
docker run --rm -it --net=metric_pipe --name=influxdb influxdb 
```

```
docker run --rm -it --net=metric_pipe --volume "$PWD"/telegraf.config:/telegraf.config:ro --name=telegraf telegraf --config /telegraf.config
```

```
docker run -u="$ID" --volume "$PWD/kapacitor-load":/data/.kapacitor/load:ro --volume "$PWD/kapacitor-tmp":/tmp/ --volume "$PWD/kapacitor-data":/var/lib/kapacitor:rw \
               --rm -it --net=metric_pipe --volume "$PWD/kapacitor.config":/etc/kapacitor/kapacitor.conf:ro --name=kapacitor kapacitor
```

Also you have to install all requirements too