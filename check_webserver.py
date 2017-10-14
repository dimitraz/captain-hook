#!/usr/bin/python3
# To do: Implement try catch blocks
# To do: Implement usability 

import subprocess

def check_webserver():
    cmd = 'ps -A | grep nginx | grep -v grep'

    try:
        status = subprocess.run(cmd, shell=True).returncode 

        if status != 0: 
            print ('Nginx not running, starting now..')
            cmd = 'sudo service nginx start'
            subprocess.run(cmd, shell=True) 
        else:
            print ('Nginx is running') 
    except Exception as e:
        error = str(e)
        print ('Error occurred:', error)

def main():
    check_webserver()

if __name__ == '__main__':
  main()
