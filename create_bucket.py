#!/usr/bin/env python3
# To do: main function?

import sys
import boto3
import datetime

boto3.setup_default_session(profile_name='boto3')
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
    create_bucket(sys.argv[1])

if __name__ == '__main__':
    main()

