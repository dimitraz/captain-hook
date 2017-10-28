#!/usr/bin/env python3
# To do: AWS profiles
# To do: sys args
# To do: use existing instance
# To do: .pem extension
# Individual boto resources?

import boto3
import sys
import time
import config
import subprocess 
from create_instance import create_instance
from create_bucket import create_bucket
from start_docker import build_image, start_container
from helpers import scp, ssh

boto3.setup_default_session(
    aws_access_key_id = config.AWS_ACCESS_KEY,
    aws_secret_access_key = config.AWS_SECRET_KEY,
    region_name = config.AWS_REGION_NAME
)
client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

def copy_files(key, dns):
    # copy the flask app and the 'check docker' script
    files = ['check_docker.py', 'helpers.py', 'flask-app/']
    print ('Copying files:', ' '.join(files))

    try:
        scp(key, dns, ' '.join(files), '.')
        scp(key, dns, 'config.py', './flask-app')
    except Exception as e:
        print ('Error occurred while copying files:', str(e))
        sys.exit(1)

def check_docker(key, dns):
    try:
        ssh(key, dns, 'cd /home/ec2-user && python3 check_docker.py')
    except Exception as e:
        print ('Error while starting check_docker script:', str(e))
        sys.exit(1)

def main(): 
    args = sys.argv[1:]
    if not args:
        print ('Usage: --key <key_name> [--ec2 <instance_name>] [--s3 <bucket_name>]')
        sys.exit(1)

    # Parse args
    key = ''
    if args[0] == '--key':
        key = args[1]
        del args[0:2]
    else:
        print ('Please provide a valid key.')
        print ('Usage: --key <key_name> [--ec2 <instance_name>] [--s3 <bucket_name>]')
        sys.exit(1)

    instance_name = ''
    if args:
        if args[0] == '--ec2':
            instance_name = args[1]
            del args[0:2]

    bucket_name = ''
    if args: 
        if args[0] == '--s3':
            bucket_name = args[1]
            del args[0:2]

    # Create an EC2 instance
    # instance = ec2.Instance('i-023e0b47256c346b9')
    # if not instance:
    instance = create_instance(key, instance_name)
    dns = instance.public_dns_name

    # Create S3 bucket
    bucket = create_bucket(bucket_name)
    bucket_name = bucket.name
    cmd = 'echo \"\nS3_BUCKET_NAME = \''  + bucket_name + '\'\" >> config.py'
    subprocess.run(cmd, shell=True)

    # Copy over flask app
    print ('Waiting for instance to initialise')
    time.sleep(60)
    copy_files(key, dns)

    # Start docker, build image, run container
    build_image(key, dns, '')
    start_container(key, dns, '')

    # Make sure docker is running
    check_docker(key, dns)

if __name__ == '__main__':
    main()