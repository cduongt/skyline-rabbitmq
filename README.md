# Skyline - RabbitMQ server

This is proof-of-concept server-client application written for Skyline software controlled by RabbitMQ. The prototype was tested in MetaCloud and it was written for [MMCI](https://www.mou.cz/en/) - Masaryk Memorial Cancer Institute.

## Installation

### Master
Centos 7
1) Install RabitMQ - https://www.rabbitmq.com/
2) Install Python 2.7
3) Install Pika AMQP client - http://pika.readthedocs.io/en/0.10.0/
4) Install Samba server
5) Download and run master.py

### Slave
Windows server 2012 R2
1) Install Python 2.7
2) Install Pika client
3) Install Skyline
4) Mount Sambu
5) Run slave.py
