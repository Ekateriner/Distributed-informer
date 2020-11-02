from flask import Flask
from flask import request
from flask import jsonify
import json
import random
import requests
import string
import sqlite3
from globaly import *
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

def create_id(size):
    id = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(size))
    return id

def get_fields_from_admin(admins_fields):
    fields = json.loads(admins_fields)
    return fields

def create_tick_task(fields):
    #fields = get_fields_from_admin(admins_fields)
    # this id may not be used
    # id = np.randint(100)
    template = fields["template"]   # determine which tick script to use
    if template == "mean":
        measure = fields.get("measurement", "cpu")
        tag = fields.get("tag", "host")
    elif template == "derivative":
        measure = fields.get("measurement", "cpu")
        tag = fields.get("tag", "*")
    elif template == "sum":
        measure = fields.get("measurement", "mem")
        tag = fields.get("tag", "host")
    info = fields.get("info", 50)
    warn = fields.get("warn", 70)
    crit = fields.get("crit", 90)

    # connecting with database
    conn = sqlite3.connect('ARGUMENTS.db')
    cur = conn.cursor()

    # checking whether task with given arguments already exists
    cur.execute('''SELECT task_id FROM ARGUMENTS WHERE template = "{}" AND measurement = "{}" AND tag = "{}"'''.format(template, measure, tag))
    row = cur.fetchall()
    # if true, won't create the same task, just save the number of the existing one
    if len(row) != 0:
        task_id = row[0]
        return task_id

    # else create new task
    TICK_SCRIPT = TYPES[template].format(measure, tag, tag, measure)
    task_id = create_id(SIZE)
    cur.execute('''INSERT INTO ARGUMENTS (task_id, template, measurement, tag) VALUES (?, ?, ?, ?)''', (task_id, template, measure, tag))
    conn.commit()
    conn.close()
    # sends tick task to kapacitor to be executed
    data = {"id": task_id,
            "type": "stream",
            "dbrps": [{"db": "telegraf", "rp": "autogen"}],
            "script": TICK_SCRIPT, 
            "vars": {
                "info": {
                    "value": info,
                    "type" : "float"
                    },
                "warn": {
                    "value": warn,
                    "type" : "float"
                    },
                "crit": {
                    "value": crit,
                    "type" : "float"
                    }
                },
            "status": "enabled"
            }
    for k_url in kapacitor_urls:
        res = requests.post(k_url + '/kapacitor/v1/tasks', json=data)
    return task_id

@app.route('/create_task', methods=['POST'])
def create_task():
    data = json.loads(request.get_data())
    task_id = create_tick_task(data)
    return task_id, "OK\n"


@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = json.loads(request.get_data())
    message = data['message']
    i = message.rfind(':')
    telegeram_id = message[i:]
    data['message'] = message[:i]
    requests.post(alert_system_url, json=data)
    return "OK\n"

@app.route('/get_running_tasks', methods=['GET'])
def get_running_tasks_ids():
    responce = requests.get(kapacitor_url + "/kapacitor/v1/tasks")
    data = json.loads(responce.json())
    task_list = list()
    for task in data["tasks"]:
        task_list.append(task["id"])
    sers = get_all_users()
    return jsonify(task_list)

@app.route('/get_patterns', methods=['GET'])
def get_patterns():
    print(TICK_PATTERNS)
    return jsonify(TICK_PATTERNS)

@app.route('/ping', methods=['GET'])
def ping():
    return "pong\n"

if __name__ == '__main__':
    app.run(host='task_creator', port=9091)

