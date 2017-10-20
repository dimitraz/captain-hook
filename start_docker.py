#!/usr/bin/python3
# To do: Implement try catch blocks
# To do: Implement usability 

from helpers import ssh, scp

def start_service():
    # Start docker if not started

def build_image():
    tag = 'captain-hook'
    cmd = 'cd /home/ec2-user/flask-app && sudo docker build -t ' + tag + ' .'
    ssh('key.pem', '34.241.48.147', cmd)

def start_container():
    tag = 'captain-hook'
    port = '80'
    cmd = 'sudo docker run -d -p ' + port + ':80 ' + tag
    ssh('key.pem', '34.241.48.147', cmd)

def main():
    build_image()
    start_container()

if __name__ == '__main__':
    main()
