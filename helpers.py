#!/usr/bin/python3

import subprocess 

# ssh into instance and perform command
def ssh(key, dns, cmd):
    ssh = 'ssh -i ' + key + ' ec2-user@' + dns + 'rm -rf check_webserver.py' + cmd
    subprocess.run(cmd, shell=True)

# copy files and folders to a given destination
def scp(key, dns, file, dest):
    cmd = 'scp -r -i ' + key + ' ' + file + ' ec2-user@' + dns + ':' + dest
    subprocess.run(cmd, shell=True)

