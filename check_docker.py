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
        print ('Error occurred:', str(e))

# Check if redis/application containers are running
def check_container():
    img = 'captain-hook'
    app = 'sudo docker ps -a -f status=running | grep ' + img
    redis = 'sudo docker ps -a -f status=running | grep redis'
    try:
        app_status = subprocess.run(app, shell=True).returncode 
        redis_status = subprocess.run(redis, shell=True).returncode 

        # Check Flask app
        if app_status != 0: 
            print ('Application not running, starting now..')
            try:
                cmd = 'sudo docker ps -a -f status=exited | grep ' + img
                status = subprocess.run(cmd, shell=True).returncode 

                if status != 0:
                    print ('Starting container from image', img)
                    port = '80'
                    cmd = 'sudo docker run --name captain-py --net py-net -d -p ' + port + ':80 ' + img
                    try:
                        subprocess.run(cmd, shell=True) 
                    except Exception as e:
                        print ('Error while starting application container:', str(e))
                else:
                    print ('Restarting Flask app container')
                    cmd = 'sudo docker start captain-py'
                    try:
                        subprocess.run(cmd, shell=True) 
                    except Exception as e:
                        print ('Error while starting application container:', str(e))
            except Exception as e: 
                 print ('Error while starting application container:', str(e))
        else:
            print ('Application is running') 

        # Check Redis 
        if redis_status != 0: 
            print ('Redis not running, starting now..')
            try: 
                cmd = 'sudo docker ps -a -f status=exited | grep redis'
                status = subprocess.run(cmd, shell=True).returncode 

                if status != 0:
                    print ('Starting redis container')
                    cmd = 'sudo docker run --name redis-py --net py-net -d redis'
                    try:
                        subprocess.run(cmd, shell=True) 
                    except Exception as e:
                        print ('Error while starting redis:', str(e))
                else:
                    print ('Restarting redis container')
                    cmd = 'sudo docker start redis-py'
                    try:
                        subprocess.run(cmd, shell=True) 
                    except Exception as e:
                        print ('Error while starting application container:', str(e))
            except Exception as e:
                print ('Error while starting redis:', str(e))
        else:
            print ('Redis is running') 
    except Exception as e:
        print ('Error occurred:', str(e))

def main():
    check_docker()
    check_container()

if __name__ == '__main__':
  main()
