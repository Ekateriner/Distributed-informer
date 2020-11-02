## Installation

```
mkdir launch
cd launch/
virtualenv -p python3.8 venv
. venv/bin/activate
git clone http://bb.prac.atp-fivt.org:8080/scm/ii/configurator.git
cd configurator/
git checkout release/II-14-django
pip install -r requirements.txt
cd cconfigurator/
./manage.py runserver 8000
```

## Links
```
http://127.0.0.1:8000/ +

admin/
api/metrics/
api/notifications/
api/recipients/
api/tags/
api/templates/
api/template_instances/
api/inventarizaion/...
```

```
login for admin:     mike
password:            cconfigurator
```

## Dump DB

После каждого изменения базы сервер отправляет POST-запрос на адрес, указанный в ```cconfigurator/config.py``` с измененными данными в json формата
```
{
  "action": "save"/"delete",
  "model": model,
  [если "delete"] "id": id,
  [если "save"] "data": json c сохраненными данными
}
```

## API

### Метрики

Получить все метрики. Можно пофильтровать по названию, единице измерения
```
   http://127.0.0.1:8000/api/metrics[?metric=<name>&unit=<unit>]
```

Добавить метрику. POST-запросом отправляем json вида 

```
{
    "name": <name> (обязательно),
    "unit": <unit> (обязательно)
}
```
```
   http://127.0.0.1:8000/api/metrics/
```

Получить (GET), удалить (DELETE) или изменить (PUT) метрику по id. Для изменения нужно отправить json по шаблону выше.
```
   http://127.0.0.1:8000/api/metrics/<id>/
```

### Пользователи

Получить всех пользователей
```
   http://127.0.0.1:8000/api/recipients/
```

Добавить пользователя. POST-запросом отправляем json вида 

```
{
    "name": <name> (обязательно),
    "phone": <phone>,
    "telegram": <telegram>,
    "id_for_bot": <chat id>,
    "id_for_matrix": <chat id>,
    "email": <email>
}
```
```
   http://127.0.0.1:8000/api/recipients/
```

Получить (GET), удалить (DELETE) или изменить (PUT) пользователя по id. Для изменения нужно отправить json по шаблону выше.
```
   http://127.0.0.1:8000/api/recipients/<id>/
```

### Теги

Получить все теги. Можно пофильтровать по названию
```
   http://127.0.0.1:8000/api/tags[?tag=<tag>]
```

Добавить тег. POST-запросом отправляем json вида 
```
{
    "name" : <name> (обязательно)
}
```
```
   http://127.0.0.1:8000/api/tags/
```

Получить (GET), удалить (DELETE) или изменить (PUT) тег по id. Для изменения нужно отправить json по шаблону выше.
```
   http://127.0.0.1:8000/api/tags/<id>
```

### Шаблоны

Получить все шаблоны. Можно пофильтровать по названию
```
   http://127.0.0.1:8000/api/templates[?template=<template>]
```

Добавить шаблон. POST-запросом отправляем json вида 
```
{
    "name" : <name> (обязательно),
    "data" : <template text>,
    "task_id" : <kapacitor task id>,
    "args" : "{arg1: description, arg2: description, ...}",
    "defaults" : "{arg1: value, arg2:value}, ...",
}
```
```
   http://127.0.0.1:8000/api/templates/
```

Получить (GET), удалить (DELETE) или изменить (PUT) шаблон по id. Для изменения нужно отправить json по шаблону выше.
```
   http://127.0.0.1:8000/api/templates/<id>
```

### Инстансы шаблонов

Получить все инстансы. Можно пофильтровать по названию шаблона и task_id
```
   http://127.0.0.1:8000/api/template_instances[?template=<template>&task_id=<task_id>]
```

Добавить инстанс. POST-запросом отправляем json вида 
```
{
    "template" : <template id> (обязательно),
    "args" : "{arg1: value, arg2:value}, ..."
}
```
```
   http://127.0.0.1:8000/api/template_instances/
```

Получить (GET), удалить (DELETE) или изменить (PUT) инстанс по id. Для изменения нужно отправить json по шаблону выше.
```
   http://127.0.0.1:8000/api/template_instances/<id>
```

### Уведомления

Получить все уведомления. Можно пофильтровать по юзеру, названию шаблона, task id, тегам
```
   http://127.0.0.1:8000/api/notifications[?user=<user>&template=<template>&task_id=<task_id>&tags=<tag1,tag2,...>]
```

Добавить уведомление. POST-запросом отправляем json вида 
```
{
    "user" : <user> (обязательно)
    "template_instance" : <template instance id> (обязательно)
    "tags" : [id1, id2, ...]
    "info" : float
    "warn" : float
    "crit" : float
}
```
```
   http://127.0.0.1:8000/api/notifications/
```

Получить (GET), удалить (DELETE) или изменить (PUT) уведомление по id. Для изменения нужно отправить json по шаблону выше.
```
   http://127.0.0.1:8000/api/notifications/<id>
```

