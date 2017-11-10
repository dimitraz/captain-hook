#!/usr/bin/env python3

import sys
from helpers import ssh, scp

def build_image(key, dns, tag):
    if not tag:
        tag = 'captain-hook'

    print ('Building Docker image with tag:', tag)
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
    cmd = 'sudo docker run --name captain-py --net py-net -d -p ' + port + ':80 ' + tag
    try:
        ssh(key, dns, cmd)
    except Exception as e:
        print ('Error occurred while building image:', str(e))

def main():
    args = sys.argv[1:]
    
    if len(args) < 3:
        print ('Please supply key, dns and image tag as first, second and third arguments')
        sys.exit(1)

    key = sys.argv[1]
    dns = sys.argv[2]
    tag = sys.argv[3]

    build_image(key, dns, tag)
    start_container(key, dns, tag)

if __name__ == '__main__':
    main()
