import sys
import json
from kapacitor.udf.agent import Agent, Handler, Server
from kapacitor.udf import udf_pb2
import signal
import logging
from TrafficPredictor import TrafficPredictor
import numpy as np

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger()


class Handler(Handler):
    class state(object):
        def __init__(self):
            self.size = 0.0
            self._dif = 0.0
            self._val = 0.0
            self._ts = 0.0
            self._pred = 0.0
            self._tp = TrafficPredictor(value_increments = np.zeros(1), 
                                        time_steps = np.zeros(1))
        
        def update(self, value, ts, dur):
            self._dif = value - self._val
            self._val = value
            self.size += 1
            self._ts = ts
            self._tp.add(np.array(self._ts), np.array(self._dif))
            if (self.size % 10 == 1):
                self._tp.transform()
# logger.info('Education')
            self._pred = self._tp.predict_quantile(0.9, int(self.size + self.size//2) + 2, dur)

            logger.info(self._pred)
            return self._pred



        def snapshot(self):
            return {
                    'dif' : self._dif,
                    'size' : self.size,
                    'val' : self._val,
                    'timestamp' : self._ts,
                    'prediction': self._pred,
                    'model': self._tp.get_data()
            }

        def restore(self, data):
            self.size = int(data['size'])
            self._val = float(data['val'])
            self._ts = float(data['timestamp'])
            self._pred = float(data['prediction'])
            self._dif = float(data['dif'])
            self._tp = TrafficPresictor().reset_data(data['model'])


    def __init__(self, agent):
        self._agent = agent
        self._field = None
        self._as = 'prediction'
        self._duration = '1m'
        self._state = {}


    def info(self):
#logger.info("Info Response")
        response = udf_pb2.Response()           
        response.info.wants = udf_pb2.STREAM
        response.info.provides = udf_pb2.STREAM
        response.info.options['field'].valueTypes.append(udf_pb2.STRING)
        response.info.options['as'].valueTypes.append(udf_pb2.STRING)
        response.info.options['duration'].valueTypes.append(udf_pb2.STRING)
        return response

    def init(self, init_req):
#logger.info("Init Response")
        response = udf_pb2.Response()
        success = True
        msg = ''

        for opt in init_req.options:
            if opt.name == 'field':
                self._field = opt.values[0].stringValue
            elif opt.name == 'as':
                self._as = opt.values[0].stringValue
            elif opt.name == 'duration':
                self._duration = opt.values[0].stringValue

        if self._field is None:
            success = False
            msg += ' must supply field name'
            logger.info('No ok')
        if self._as == '':
            success = False
            msg += ' invalid as name'
            logger.info('No ok')

        response = udf_pb2.Response()
        response.init.success = success
        response.init.error = msg[1:]
                    
        return response

    def snapshot(self):
#logger.info("Snapshot Response")
        data = {}
        for group, state in zip(self._state.keys(), self._state.values()):
            data[group] = state.snapshot()

        response = udf_pb2.Response()
#response.snapshot.snapshot = json.dumps(data)
        return response

    def restore(self, restore_req):
#logger.info("Restore Response")
        success = False
        msg = ''
        try:
            data = json.loads(restore_req.snapshot)
            for group, snapshot in data.iteritems():
                self._state[group] = Handler.state(0)
                self._state[group].restore(snapshot)
            success = True
        except Exception as e:
            success = False
            msg = str(e)

        response = udf_pb2.Response()
        response.restore.success = success
        response.restore.error = msg

        return response

    def begin_batch(self, begin_req):
#logger.info("BBatch Response")
        raise Exception("not supported")

    def point(self, point):
#logger.info("Point Response")
        response = udf_pb2.Response()
        response.point.CopyFrom(point)

        response.point.ClearField('fieldsInt')
        response.point.ClearField('fieldsString')
        response.point.ClearField('fieldsDouble')

#logger.info(self._field)

        value = point.fieldsDouble[self._field]
        time = point.time
        if point.group not in self._state:
           self._state[point.group] = Handler.state()
        prediction = self._state[point.group].update(value, time, 60)

        response.point.fieldsDouble[self._as] = prediction
        self._agent.write_response(response, True)

    def end_batch(self, end_req):
#logger.info("EBatch Response")
        raise Exception("not supported")

class accepter(object):
    _count = 0
    def accept(self, conn, addr):
        self._count += 1
        a = Agent(conn, conn)
        h = Handler(a)
        a.handler = h

        logger.info("Starting Agent for connection %d", self._count)
        a.start()
        a.wait()
        logger.info("Agent finished connection %d",self._count)

if __name__ == '__main__':
    path = "/tmp/predict.sock"
    if len(sys.argv) == 2:
        path = sys.argv[1]
    server = Server(path, accepter())
    logger.info("Started server")
    server.serve()
