#!/usr/bin/python3
# To do: AWS profiles
# To do: sys args
# To do: use existing instance

import boto3
import sys
import create_instance 
import start_docker
import check_docker
from helpers import scp, ssh

def copy_files(key, dns):
    # copy the flask app and the 'check docker' script
    scp(key, dns, 'check_docker.py helpers.py flask-app/', '.')

def parse_args():
    # parse user args

def main(): 
    # Create an EC2 instance
    create_instance.main()

    # Copy over flask app
    copy_files()

    # Start docker, build image, run container
    start_docker.main()

    # Make sure docker is running
    check_docker.main()