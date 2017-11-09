#!/usr/bin/env python3

import sys
import boto3
import datetime
import config

boto3.setup_default_session(
    aws_access_key_id = config.AWS_ACCESS_KEY,
    aws_secret_access_key = config.AWS_SECRET_KEY,
    region_name = config.AWS_REGION_NAME
)
s3client = boto3.client('s3')
s3 = boto3.resource('s3')

def create_bucket(bucket_name): 
    if not bucket_name:
        bucket_name = '{0:%Y-%m-%d-%H.%M.%S-hook}'.format(datetime.datetime.now())

    try:
        bucket = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'}
        )
        print ('Bucket created with name:', bucket.name)
        return bucket
    except Exception as e:
        print ('Error occurred while creating bucket:', str(e))
        sys.exit(1)

def main():
    args = sys.argv[1:]
    if not args:
        create_bucket('')
    else:
        create_bucket(sys.argv[1])

if __name__ == '__main__':
    main()

