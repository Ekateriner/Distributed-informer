import sys
import json
from kapacitor.udf.agent import Agent, Handler, Server
from kapacitor.udf import udf_pb2
import signal
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger()

# Mirrors all points it receives back to Kapacitor
class MirrorHandler(Handler):                   #handler (process requests)
    def __init__(self, agent):                  #init = save agent
        self._agent = agent

    def info(self):                             
        response = udf_pb2.Response()           
        response.info.wants = udf_pb2.STREAM    #input format
        response.info.provides = udf_pb2.STREAM #output format
        return response

    def init(self, init_req):                   #init response
        response = udf_pb2.Response()
        response.init.success = True
        return response

    def snapshot(self):                         #snapshor state
        logger.info('Snap')
        response = udf_pb2.Response()
        response.snapshot.snapshot = ('').encode()
        return response

    def restore(self, restore_req):
        logger.info('Restore')
        response = udf_pb2.Response()
        response.restore.success = False
        response.restore.error = 'not implemented'
        return response

    def begin_batch(self, begin_req):           #batch?
        raise Exception("not supported")

    def point(self, point):                     #single row
        response = udf_pb2.Response()
        response.point.CopyFrom(point)
        logger.info(point)
        self._agent.write_response(response, True) #response / flush

    def end_batch(self, end_req):               #batch end?
        raise Exception("not supported")

class accepter(object):                     #class for server config
    _count = 0
    def accept(self, conn, addr):           #new connection
        count = self._count
        self._count += 1                    #count of connection
        a = Agent(conn, conn)               #create agent (communicate with kapacitor) in/out
        h = MirrorHandler(a)                #create handler
        a.handler = h                       #save handler to agent

        logger.info("Starting Agent for connection %d", count) #start log
        a.start()                           #start agent
        a.wait()                            #wait request
        logger.info("Agent finished connection %d", count)      #end log

if __name__ == '__main__':
    path = "/tmp/mirror.sock"           #path to socket
    if len(sys.argv) == 2:              #or we use argv for path
        path = sys.argv[1]
    server = Server(path, accepter())   #create server
    logger.info("Started server")       #log the start
    server.serve()                      #run server
