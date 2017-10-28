#!/usr/bin/env python3
# To do: Check if image exists / just start container
# To do: custom docker tag? 

import subprocess
from helpers import ssh, scp

# Check if the docker daemon is running
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

# Check if redis/application containers are running
def check_container():
    tag = 'captain-hook'
    app = 'sudo docker ps -a | grep ' + tag
    redis = 'sudo docker ps -a | grep redis'
    try:
        app_status = subprocess.run(app, shell=True).returncode 
        redis_status = subprocess.run(redis, shell=True).returncode 

        if app_status != 0: 
            
            print ('Application not running, starting now..')
            print ('Starting container from image', tag)
            port = '80'
            cmd = 'sudo docker run --name captain-py --net py-net -d -p ' + port + ':80 ' + tag
            try:
                subprocess.run(cmd, shell=True).returncode 
            except Exception as e:
                print ('Error while starting application container:', str(e))
        else:
            print ('Application is running') 

        if redis_status != 0: 
            print ('Redis not running, starting now..')
            cmd = 'sudo docker run --name redis-py --net py-net -d redis'
            try:
                subprocess.run(cmd, shell=True).returncode 
            except Exception as e:
                print ('Error while starting redis:', str(e))
        else:
            print ('Redis is running') 
    except Exception as e:
        error = str(e)
        print ('Error occurred:', error)

def main():
    check_docker()
    check_container()

if __name__ == '__main__':
  main()
