#!/usr/bin/env python
import pika
import os
import time
import logging

DIR_SAMBA = '/samba/share/'
logging.basicConfig(filename=DIR_SAMBA + 'master.log',level=logging.DEBUG)

while True:
	for filename in os.listdir(DIR_SAMBA):
		if filename.endswith('sky'):
			if not os.path.exists(DIR_SAMBA + filename + 'd') and not os.path.exists(DIR_SAMBA + filename + '.progress'):
				credentials = pika.PlainCredentials('xxx', 'xxx')
				connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
				channel = connection.channel()
				channel.queue_declare(queue='work')
				channel.basic_publish(exchange='', routing_key='work', body=filename)
				open(DIR_SAMBA + filename + '.progress', 'w').close()
				logging.debug(time.strftime('%H:%M:%S') + ' [x] Processing file ' + filename)
				channel.close()
				connection.close()
	logging.debug(time.strftime('%H:%M:%S') + ' Master server is up')
	time.sleep(180)
