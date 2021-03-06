# Skyline - RabbitMQ server

This is proof-of-concept server-client application written for Skyline software controlled by RabbitMQ. The prototype was tested in MetaCloud and it was written for [MMCI](https://www.mou.cz/en/) - Masaryk Memorial Cancer Institute.

## License
- Code of maste.py and slave.py - MIT license
- Python 2.7                    - GPL-compatible
- RabbitMQ                      - Mozilla public license
- Pika                          - BSD 3-clause
- Skyline                       - Apache 2.0

## Installation

### Master
Centos 7
1) Install RabbitMQ - https://www.rabbitmq.com/
- Install EPEL repo if not present: yum install epel-release
- Update repo cache: yum update
- Install rabbitmq-server: yum install rabbitmq-server
- Enable rabbitmq on startup: chkconfig rabbitmq-server on
- systemctl enable rabbitmq-server
- systemctl start rabbitmq-server
- rabbitmqctl add_user test test
- rabbitmqctl set_user_tags test administrator
- rabbitmqctl set_permissions -p / test ".*" ".*" ".*"
- firewall-cmd --permanent --add-port=5672/tcp
- firewall-cmd --reload

2) Install Python 2.7
- cd /usr/src
- yum install gcc
- wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
- tar xzf Python-2.7.10.tgz
- cd Python-2.7.10
- ./configure
- make altinstall

3) Install Pika AMQP client - http://pika.readthedocs.io/en/0.10.0/
- yum -y update
- yum -y install python-pip
- pip install pika

4) Install Samba server
- yum install samba samba-client samba-common
- nano /etc/samba/smb.conf<br/>
[global]<br/>
workgroup = IT<br/>
server string = Samba Server %v<br/>
netbios name = egi_master<br/>
security = user<br/>
map to guest = bad user<br/>
dns proxy = no<br/>
#============================ Share Definitions ==============================<br/>
[Anonymous]<br/>
path = /samba/anonymous<br/>
browsable = yes<br/>
writable = yes<br/>
guest ok = yes<br/>
read only = no<br/>
[secured]<br/>
path = /samba/secured<br/>
valid users = @smbgrp<br/>
guest ok = no<br/>
writable = yes<br/>
browsable = yes<br/>
- mkdir -p /samba/anonymous
- systemctl enable smb.service
- systemctl restart smb.service
- firewall-cmd --permanent --zone=public --add-service=samba
- firewall-cmd --reload
- cd /samba
- chmod -R 0755 anonymous/
- chown -R nobody:nobody anonymous/
- chcon -t samba_share_t anonymous/
- groupadd smbgrp
- useradd samba -G smbgrp
- smbpasswd -a samba
- mkdir -p /samba/secured
- chmod -R 0777 secured/
- chown -R samba:smbgrp secured/
- chcon -t samba_share_t secured/
- systemctl restart nmb.service
- systemctl restart smb.service

5) Python master script
- mkdir /home/skyline
- cd /home/skyline
- wget master.py ... source github ...
- nano master.py <br/>EDIT:<br/>
DIR_SAMBA - e.g. /samba/secured<br/>
pika.PlainCredentials - must match rabbitMQ credentials
- FOR TESTING: nohup python -u /home/skyline/master.py > master.log &
- AUTO START: crontab -e<br/>
@reboot /home/skyline/master.py

### Slave
Windows server 2012 R2
1) Install Python 2.7
- Download and install latest version of Python 2.7.x from https://www.python.org/downloads/
2) Install Pika client
- Install pip first - CMD, python get-pip.py
- pip install pika
3) Install Skyline
- Download from: https://skyline.ms/project/home/software/Skyline/begin.view and install
4) Mount shared folder (located on samba server)
5) Slave.py
- Download slave.py from github
- EDIT slave.py so it matches configuration <br/>
DIR_SAMBA         - variable must match samba configuration <br/>
IP_MASTER         - must match IP address of master node<br/>
SKYLINE_EXE       - must match the path to SkylineRunner.exe<br/>
Pika credentials  - must match configuration of pika on master node<br/>
- start slave.py automatically during logon <br/>
RUN shell:startup<br/>
CREATE FILE python_startup.bat<br/>
INSERT python <path_to_python.py><br/>

## User manual (wokstation)
1) Download and  Install Skyline
- Source: https://skyline.ms/project/home/software/Skyline/begin.view 
2) Mount shared folder (located on master node)
3) Prepare your own analysis in skyline or download testing data from the repository
4) Copy .sky file and folder with data (named /data) into shared folder.
5) Process
- Task has been noticed by master node when the .progress file is created
- Temporary files are created when the task is started on the worker node
- .skyd file is created when the task is finished
- Info/debug or error messages are stored in master.log or worker.IP.log files
6) Now you can open .sky file with the results (chromatographs)

