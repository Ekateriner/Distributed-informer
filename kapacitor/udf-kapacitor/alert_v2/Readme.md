# Predictor

Predict quntile of field

## Getting Started

1. Add folders to kapacitor-load
2. Add to kapacitor.conf 
    ```
    [udf]
    [udf.functions]
      [udf.functions.tag_add]
          socket = "tmp/tag_add.sock"
          timeout = "10s"
    ```
3. Use docker build to create server image:
    ```
    docker rmi server
    docker build kapacitor-load/server/ -t server
    
    ```
4. To run server image use:
    ```
    docker run -u="$ID" --volume "$PWD/kapacitor-load/sideloadFiles":/data/.kapacitor/load/sideloadFiles:ro --volume "$PWD/kapacitor-tmp":/tmp/ --rm -it --net=metric_pipe --name=server server
    ```
5. Run all images

_Remark_:
File with critical levels has format json. It's list with dictionares (`{'level_id': id, 'info': info, 'infoReset': infoReset, ...}`)

### Updating levels

1. Run comand line in server docker:
    ```
    docker exec -u 0 -it server ash
    ```
2. Use comands to create post http:
    ```
    curl -d '{"task_id": id, "level_id": "old\new_level_id", \
                (_optional_) "info": new_info, "infoReset": new_infoReset ...,
                (_or_) "source": "new_source"}' -X POST server:9000/{command}
    ```
3. There are next commands:
    * \add - add new level_id and levels or update old one
    * \delete - delete levels by level_id
    * \update - delete all levels and create new dict from given source
4.  task_id must be provided - the indificator of task, which uses these group of levels

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

## Deployment

### TO DO:
- More math functions in formula
- Tune messages
- Add file updates through some period
