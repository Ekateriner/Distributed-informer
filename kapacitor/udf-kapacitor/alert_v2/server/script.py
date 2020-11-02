import sys
import getopt
import json
from kapacitor.udf.agent import Agent, Handler, Server
from kapacitor.udf import udf_pb2
import signal
import logging
import re
from flask import Flask, request, jsonify
import requests
from threading import Lock, Thread

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger()

app = Flask(__name__)
processes = []
server_lock = Lock() 

# Mirrors all points it receives back to Kapacitor
class Handler(Handler):
    def __init__(self, agent, file_path):
        self._agent = agent
        self._path = file_path
        self._id = None
        self._source = None
        self._data = None
        self._agent_lock = Lock()

    def decode_json(self, dct):
        self._data[dct['level_id']] = {'info': dct['info'], 'infoReset': dct['infoReset'], \
                                       'warn': dct['warn'], 'warnReset': dct['warnReset'], \
                                       'crit': dct['crit'], 'critReset': dct['critReset']}

    def update_source(self, source = None):
        if not(source is None):
            self._source = source

        self._data = {}
        with open("{}/{}".format(self._path, self._source), 'r') as data_json:
            json.loads(data_json.read(), object_hook=self.decode_json)

    def add_id(self, level_id, info, infoReset, warn, warnReset, crit, critReset):
        self._data[level_id] = {'info': info, 'infoReset': infoReset, \
                                'warn': warn, 'warnReset': warnReset, \
                                'crit': crit, 'critReset': critReset}

    def del_id(self, level_id):
        del self._data[level_id]

    def info(self):
        response = udf_pb2.Response()           
        response.info.wants = udf_pb2.STREAM
        response.info.provides = udf_pb2.STREAM
        response.info.options['source'].valueTypes.append(udf_pb2.STRING)
        response.info.options['task_id'].valueTypes.append(udf_pb2.INT)
        return response

    def init(self, init_req):                   #init response
#logger.info("Init Response")
        response = udf_pb2.Response()
        success = True
        msg = ''

        for opt in init_req.options:
            if opt.name == 'source':
                self._agent_lock.acquire()
                self._source = opt.values[0].stringValue
                self._agent_lock.release()
            elif opt.name == 'task_id':
                self._id = opt.values[0].intValue

        if self._source is None:
            success = False
            msg += ' must supply source'
            logger.info('Init error')

        if self._id is None:
            success = False
            msg += ' must supply task_id'
            logger.info('Init error')

        response = udf_pb2.Response()
        response.init.success = success
        response.init.error = msg[1:]
        
        if success:
            self._agent_lock.acquire()
            self.update_source()
            self._agent_lock.release()

        return response

    def snapshot(self):
        logger.info('Snapshot')
        response = udf_pb2.Response()
        self._agent_lock.acquire()
        response.snapshot.snapshot = json.dumps(self._data).encode()
        self._agent_lock.release()
        return response


    def restore(self, restore_req):             #restore ?
        success = False
        msg = ''
        
        try:
            self._agent_lock.acquire()
            self._data = json.loads(restore_req.snapshot.decode())
            self._agent_lock.release()
            success = True
        except Exception as e:
            success = False
            msg = str(e)

        response = udf_pb2.Response()
        response.restore.success = success
        response.restore.error = msg

        return response

    def begin_batch(self, begin_req):
        logger.info("BBatch Response")
        raise Exception("not supported")

    def point(self, point):
#logger.info("Point Response")
        response = udf_pb2.Response()
        response.point.CopyFrom(point)
       
        self._agent_lock.acquire()
        for lev_id, row in self._data.items():
            response.point.tags['level_id'] = str(lev_id)
            response.point.tags['info'] = str(row['info'])
            response.point.tags['infoReset'] = str(row['infoReset'])
            response.point.tags['warn'] = str(row['warn'])
            response.point.tags['warnReset'] = str(row['warnReset'])
            response.point.tags['crit'] = str(row['crit'])
            response.point.tags['critReset'] = str(row['critReset'])
            self._agent.write_response(response, True) #response / flush
        self._agent_lock.release()

    def end_batch(self, end_req):               #batch end?
        logger.info("EBatch Response")
        raise Exception("not supported")

class accepter(object):
    def __init__(self, processes, lock, file_path):
        self._count = 0
        self._path = file_path
        self._processes = processes
        self._lock = lock

    def accept(self, conn, addr):
        self._count += 1
        a = Agent(conn, conn)
        h = Handler(a, self._path)
        a.handler = h
        
        self._lock.acquire()
        self._processes.append(a)
        self._lock.release()

        logger.info("Starting Agent for connection %d", self._count)
        a.start()
        a.wait()
        logger.info("Agent finished connection %d",self._count)
        self._processes.remove(a)

@app.route('/add', methods=['POST'])
def add_id():
    data = json.loads(request.get_data())
    update(data['task_id'], 'add', data['level_id'], 
            data['info'], data['infoReset'], 
            data['warn'], data['warnReset'],
            data['crit'], data['critReset'])
    return 'OK\n'

@app.route('/delete', methods=['POST'])
def del_id():
    logger.info(request.json)
    data = json.loads(request.get_data())
    update(data['task_id'], 'del', data['level_id'])
    return 'OK\n'

@app.route('/update', methods=['POST'])
def update():
    data = json.loads(request.get_data())
    update(data['task_id'], 'upd', source=data['source'])
    return 'OK\n'

def update(task_id, act='add', level_id=None, 
            info=None, infoReset=None, 
            warn=None, warnReset=None, 
            crit=None, critReset=None, source=None):
    server_lock.acquire()
    for agent in processes:
        if agent.handler._id == task_id:
            agent.handler._agent_lock.acquire()
            if(act == 'add'):
                agent.handler.add_id(level_id, info, infoReset, warn, warnReset, crit, critReset)
            elif(act == 'del'):
                agent.handler.del_id(level_id)
            elif(act == 'upd'):
                agent.handler.update_source(source)
            agent.handler._agent_lock.release()

    server_lock.release()
    return 0

if __name__ == '__main__':
    sock_path = "/tmp/tag_add.sock"
    file_path = '/data/.kapacitor/load/sideloadFiles'

    opts, args = getopt.getopt(sys.argv[1:], "s:p:",["socket=","path="])

    for opt, arg in opts:
        if opt in ("-s", "--socket"):
            sock_path = arg
        elif opt in ("-p", "--path"):
            file_path = arg

    if len(sys.argv) == 2:
        path = sys.argv[1]
    server = Server(sock_path, accepter(processes, server_lock, file_path))
    logger.info("Started server")

    http_thread = Thread(target=app.run, args=('server', 9000))
    server_thread = Thread(target=server.serve)
    
    server_thread.start()
    http_thread.start()
