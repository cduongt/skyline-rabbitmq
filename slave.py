import pika
import time
import socket
import logging
import os
import subprocess

hostname = socket.gethostname()
IP_SLAVE = socket.gethostbyname(hostname)
IP_MASTER = 'xxx.xxx.xxx.xxx'
DIR_SAMBA = 'Z:\\'
SKYLINE_EXE = 'C:\Users\Administrator\Downloads\Skyline\Skyline\SkylineRunner.exe'
LOG_FILENAME = DIR_SAMBA + 'worker.' + IP_SLAVE + '.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

credentials = pika.PlainCredentials('xxx', 'xxx')
connection = pika.BlockingConnection(pika.ConnectionParameters(IP_MASTER,5672,'/',credentials,socket_timeout=20))
channel = connection.channel()

channel.queue_declare(queue='work')

def callback(ch, method, properties, body):
    logging.debug(time.strftime('%H:%M:%S') + ' [x] Received ' + body)
    logging.debug(time.strftime('%H:%M:%S') + ' [x] Executing task ' + body)
    logging.debug(time.strftime('%H:%M:%S') + (subprocess.check_output(
    SKYLINE_EXE + ' --in="' + DIR_SAMBA + body + '" --import-all="' + DIR_SAMBA + 'data" --save', shell=True)).decode('ascii'))
    if os.path.exists(DIR_SAMBA + body + '.progress'):
        os.remove(DIR_SAMBA + body + '.progress')
    
channel.basic_consume(callback,
                      queue='work',
                      no_ack=True)

logging.debug(time.strftime('%H:%M:%S')+ ' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
