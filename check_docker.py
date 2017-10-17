#!/usr/bin/python3
# To do: Implement try catch blocks
# To do: Implement usability 

import subprocess
from helpers import ssh, scp

def check_docker():
    cmd = 'cd /home/ec2-user/ && ps -A | grep docker | grep -v grep'

    try:
        status = subprocess.run(cmd, shell=True).returncode 

        if status != 0: 
            print ('Docker daemon not running, starting now..')
            cmd = 'sudo service docker start'
            subprocess.run(cmd, shell=True) 
        else:
            print ('Docker is running') 
    except Exception as e:
        error = str(e)
        print ('Error occurred:', error)

def build_image():
    tag = 'captain-hook'
    cmd = 'cd /home/ec2-user/flask-app && sudo docker build -t ' + tag + ' .'
    ssh('key.pem', '34.241.48.147', cmd)

def start_container():
    tag = 'captain-hook'
    port = '80'
    cmd = 'sudo docker run -d -p ' + port + ':80 ' + tag
    ssh('key.pem', '34.241.48.147', cmd)

def check_container():
    tag = 'captain-hook'
    cmd = 'sudo docker ps -a | grep ' + tag

    try:
        status = subprocess.run(cmd, shell=True).returncode 

        if status != 0: 
            print ('Container not running, starting now..')
            build_image()
            start_container()
        else:
            print ('Container is running') 
    except Exception as e:
        error = str(e)
        print ('Error occurred:', error)

def main():
    check_docker()
    check_container()

if __name__ == '__main__':
  main()
