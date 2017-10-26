#!/usr/bin/python3
# To do: Implement usability 

import sys
from helpers import ssh, scp

#def start_service():
    # Start docker if not started

def build_image(key, dns, tag):
    if not tag:
        tag = 'captain-hook'

    print('Building Docker image with tag:', tag)
    cmd = 'cd /home/ec2-user/flask-app && sudo docker build -t ' + tag + ' .'

    try:
        ssh(key, dns, cmd)
        ssh(key, dns, 'docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)')
        ssh(key, dns, 'docker network create py-net')
        ssh(key, dns, 'docker run --name redis-py --net py-net -d redis')
    except Exception as e:
        print ('Error occurred while building image:', str(e))

def start_container(key, dns, tag):
    if not tag:
        tag = 'captain-hook'

    print('Starting container from image', tag)
    port = '80'
    cmd = 'sudo docker run --net py-net -d -p ' + port + ':80 ' + tag
    try:
        ssh(key, dns, cmd)
    except Exception as e:
        print ('Error occurred while building image:', str(e))

def main():
    key = sys.argv[1]
    dns = sys.argv[2]
    tag = sys.argv[3]

    build_image(key, dns, tag)
    start_container(key, dns, tag)

if __name__ == '__main__':
    main()
