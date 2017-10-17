#!/usr/bin/python3
# To do: Implement try catch blocks
# To do: Implement usability 

import subprocess

def check_docker():
    cmd = 'ps -A | grep docker | grep -v grep'

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

def main():
    check_docker()

if __name__ == '__main__':
  main()
