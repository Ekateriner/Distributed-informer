# UDF

Universal solution to handle metrics (from outsource functions) using udf

## Getting Started

1. Add folders to kapacitor-load
2. Add to kapacitor.conf 
    ```
    [udf]
    [udf.functions]
      [udf.functions.mirror]
          socket = "tmp/mirror.sock"
          timeout = "10s"
    ```
3. Use docker build to create server image:
    ```
    docker rmi server
    docker build kapacitor-load/server/ -t server
    ```
4. To run server image use:
    ```
    docker run -u="$ID" --volume "$PWD/kapacitor-tmp":/tmp/ --rm -it --net=metric_pipe --name=server server
    ```
5. Run all images

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
docker run -u="$ID" --volume "$PWD/kapacitor-load":/data/.kapacitor/load:ro --volume "$PWD/kapacitor-tmp":/tmp/ --volume "$PWD/kapacitor-data":/var/lib/kapacitor:rw --rm -it --net=metric_pipe --volume "$PWD/kapacitor.config":/etc/kapacitor/kapacitor.conf:ro --name=kapacitor kapacitor
```

_Remark_: 
* kapacitor-load - shared directory with scripts and templates;
* kapacitor-tmp - shared directory with sockets
* kapacitor.config and telegraf.conf - config files
* metric_pipe - docker net, that is used by all this images
