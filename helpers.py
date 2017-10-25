#!/usr/bin/python3

import subprocess 
import sys

# ssh into instance and perform command
def ssh(key, dns, cmd):
    ssh = 'ssh -o StrictHostKeyChecking=no -i ' + key + '.pem ec2-user@' + dns + ' \'' + cmd + '\''
    try: 
        subprocess.run(ssh, shell=True)
    except Exception as e:
        print ('Error while connecting to host:', str(e))
        sys.exit(1)

# copy files and folders to a given destination
def scp(key, dns, file, dest):
    cmd = 'scp -o StrictHostKeyChecking=no -r -i ' + key + '.pem ' + file + ' ec2-user@' + dns + ':' + dest
    try: 
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print ('Error while connecting to host:', str(e))
        sys.exit(1)

