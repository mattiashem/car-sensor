#
#
#  Feeder of Data !!
#  Feer of data to api 
#
#  Read from que and send data to the api endpoint for storage

import urllib.request
import json
import pika
import time
import socket
from sendFirebase import *


 


def wait_net_service(server, port, timeout=None):
	""" Wait for network service to appear 
	    @param timeout: in seconds, if None or 0 wait forever
	    @return: True of False, if timeout is None may return only True or
	             throw unhandled network exception
	"""
	while True:
		result=""
		try:
			connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
			channel = connection.channel()
			print("Connected")
			return
		except:
			print("Service not up")
			time.sleep(10)



#Wait untill we have service up
wait_net_service('rabbitmq',5672)




connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',heartbeat_interval=500))
channel = connection.channel() 




channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print("Send data to DB")
    adddataFirebase(body)
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()

#data ={"airport":"arlanda","run":"name","data":{"temp":"34","brushlenght":"20","power":"300"}}
#send_data(data,'http://localhost:8080/do/action')
