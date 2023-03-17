import signal
import queue
import struct
import threading
import time
import sys, os
import logging
from pathlib import Path

sys.path.append(os.path.join(Path(__file__).parents[0], "mqttsnclient"))
# sys.path.append(os.path.join(sys.path[0], "mqttsnclient"))

from mqttsnclient.MQTTSNclient import Callback
from mqttsnclient.MQTTSNclient import Client
from mqttsnclient.MQTTSNclient import publish
import mqttsnclient.MQTTSN as MQTTSN

FORMAT = '%(asctime)s, %(levelname)s, %(filename)s:%(lineno)d, %(funcName)s(), %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

myLogger = logging.getLogger()

print(sys.version_info)


class MyCallback(Callback):

    def on_message(self, client, TopicId, Topicname, payload, qos, retained,
                   msgid):
        m= "Arrived" +" topic  " +str(TopicId)+ "message " +\
           str(payload) +"  qos= " +str(qos) +" ret= " +str(retained)\
           +"  msgid= " + str(msgid)
        myLogger.info(m)
        myLogger.info("got the message " + str(payload))
        # message_q.put(payload)
        return True


# message_q = queue.Queue()

host = "192.168.100.109"
port = 1884
topic = "ab"
client_name = "testpub"
qos = 0

client = Client(client_name)
client.message_arrived_flag = False
client.registerCallback(MyCallback())
myLogger.info("threads {}".format(threading.active_count()))
myLogger.info("connecting {}".format(host))
client.connected_flag = False

client.connect(host, port)

client.lookfor(MQTTSN.CONNACK)
try:
    if client.waitfor(MQTTSN.CONNACK) == None:
        myLogger.info("connection failed")
        raise SystemExit("no Connection quitting")
except Exception as e:
    logging.exception(e)
    myLogger.info("connection failed")
    raise SystemExit("no Connection quitting")

# publish
try:
    for i in range(0, 10):
        msg = "test" + str(i)
        client.publish(topic, msg, qos=qos)
        time.sleep(0.5)
except BaseException as e:
    client.loop_stop()
    client.disconnect()
    raise e