import sys
import json
from kapacitor.udf.agent import Agent, Handler, Server
from kapacitor.udf import udf_pb2
import signal
import logging
import re

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger()

# Mirrors all points it receives back to Kapacitor
class Handler(Handler):
    def __init__(self, agent):
        self._agent = agent
        self._path = 'file:///data/.kapacitor/load/sideloadFiles'
        self._source = None
        self._formula = None
        self._eval = ''
        self._levels = []
        self._messages = []
        self._vars = []

    def parse_formula(self):
        _var = list(filter(None, re.split('[()+/\-* ]', self._formula)))
        _op = re.findall('[()+\-/* ]+', self._formula)

        for i in range(len(_var)):
            if re.fullmatch('\d+', _var[i]) is None:
                _var[i] = 'point.fieldsDouble[\'{}\']'.format(_var[i])

        if _op[0] == '(':
            for i in range(len(_var)):
                self._eval = '{}{}{}'.format(self._eval, _op[i], _var[i])
        else:
            for i in range(len(_var) - 1):
                self._eval = '{}{}{}'.format(self._eval, _var[i], _op[i])
            self._eval = '{}{}'.format(self._eval, _var[len(_var) - 1])
        
        if _op[len(_op) - 1] == ')':
            self._eval = '{})'.format(self._eval)

        self._vars = _var


    def parse_file(self):
        self._levels = []
        self._messages = []
        data = open("/data/.kapacitor/load/sideloadFiles/{}".format(self._source), 'r')
        for line in data:
            level, message = line.split('\t')
            self._levels.append(int(level))
            self._messages.append(message)

        data.close()

    def info(self):
        response = udf_pb2.Response()           
        response.info.wants = udf_pb2.STREAM
        response.info.provides = udf_pb2.STREAM
        response.info.options['source'].valueTypes.append(udf_pb2.STRING)
        response.info.options['formula'].valueTypes.append(udf_pb2.STRING)
        return response

    def init(self, init_req):                   #init response
#logger.info("Init Response")
        response = udf_pb2.Response()
        success = True
        msg = ''

        for opt in init_req.options:
            if opt.name == 'source':
                self._source = opt.values[0].stringValue
            elif opt.name == 'formula':
                self._formula = opt.values[0].stringValue

        if self._source is None:
            success = False
            msg += ' must supply source'
            logger.info('No ok')
        if self._formula is None:
            success = False
            msg += ' must supply formula'
            logger.info('No ok')

        response = udf_pb2.Response()
        response.init.success = success
        response.init.error = msg[1:]
        
        if success:
            self.parse_formula()
            self.parse_file()

        return response

    def snapshot(self):                         #snapshor state
#logger.info("Snapshot Response")
        response = udf_pb2.Response()
        return response

    def restore(self, restore_req):             #restore ?
#logger.info("Restore Response")
        return response

    def begin_batch(self, begin_req):           #batch?
#logger.info("BBatch Response")
        raise Exception("not supported")

    def point(self, point):                     #single row
#logger.info("Point Response")
        response = udf_pb2.Response()
        response.point.CopyFrom(point)
       
        point.fieldsDouble.update(point.fieldsInt)
        
        response.point.fieldsDouble['formula result'] = eval(self._eval)
#logger.info(response.point.fieldsDouble['formula result'])

        for i in range(len(self._levels)):
            response.point.fieldsDouble['critical_level'] = self._levels[i]
            response.point.fieldsString['message'] = self._messages[i]
            self._agent.write_response(response, True) #response / flush

    def end_batch(self, end_req):               #batch end?
#logger.info("EBatch Response")
        raise Exception("not supported")

class accepter(object):                     #class for server config
    _count = 0
    def accept(self, conn, addr):           #new connection
        self._count += 1                    #count of connection
        a = Agent(conn, conn)               #create agent (communicate with kapacitor) in/out
        h = Handler(a)                      #create handler
        a.handler = h                       #save handler to agent

        logger.info("Starting Agent for connection %d", self._count) #start log
        a.start()                           #start agent
        a.wait()                            #wait request
        logger.info("Agent finished connection %d",self._count)      #end log

if __name__ == '__main__':
    path = "/tmp/alert.sock"           #path to socket
    if len(sys.argv) == 2:              #or we use argv for path
        path = sys.argv[1]
    server = Server(path, accepter())   #create server
    logger.info("Started server")       #log the start
    server.serve()                      #run server
