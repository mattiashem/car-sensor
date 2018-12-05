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


def send_data(data, endpoint):
	'''
	Send the data to en endpoint api
	'''
	print(data)
	req = urllib.request.Request(endpoint)
	req.add_header('Content-Type', 'application/json; charset=utf-8')
	jsondata = json.dumps(str(data))
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
	
	#Send data to API
	req.add_header('Content-Length', len(jsondataasbytes))
	response = urllib.request.urlopen(req, data)
	print(response.getcode())

	if response.getcode() == 200:
		print("sent")
	else:
		print("Error send back to que")


channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print("Send data to DB")
    send_data(body,'http://api_deployer:8080/do/action')
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()

#data ={"airport":"arlanda","run":"name","data":{"temp":"34","brushlenght":"20","power":"300"}}
#send_data(data,'http://localhost:8080/do/action')