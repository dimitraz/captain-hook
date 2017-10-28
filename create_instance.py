#!/usr/bin/env python3

import boto3
import sys
import time
import config

boto3.setup_default_session(
    aws_access_key_id = config.AWS_ACCESS_KEY,
    aws_secret_access_key = config.AWS_SECRET_KEY,
    region_name = config.AWS_REGION_NAME
)
client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

# Read file to load in as user data
def user_data():
    try:
        f = open('user-data.sh', 'rU')
        data = f.read()
        f.close()
        return data
    except IOError as e:
        print ('Cannot read user data:', str(e))
        sys.exit(1)

# Configure security group
def security_group():
    group_name = 'http_ssh'
    group_desc = 'Allow incoming http and ssh traffic'

    # If security group exists, get group id
    groups = [(sg.group_name, sg.group_id) for sg in ec2.security_groups.all()]

    # Return security groups with name matching group_name
    # sg is a tuple of (group_name, group_id)
    group = [(sg[0], sg[1]) for sg in groups if sg[0] == group_name]
    if group:
        # First item in array, first item in tuple
        group_id = group[0][0]
        print ('Using existing security group with id %s' % (group_id))

        return group_id

    # Otherwise, create security group
    else: 
        try:
            group = ec2.create_security_group(
                GroupName=group_name,
                Description=group_desc
            )
            
            group_id = group.id
            print ('Security Group created with id %s' % (group_id))

            response = group.authorize_ingress(
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 80,
                        'ToPort': 80,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    },
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }
                ]
            )

            print ('Ingress rules successfully added')
            return group_id
        except Exception as e:
            print ('Error occurred while creating security group:', str(e))
            sys.exit(1)

# Create the instance
def create_instance(key, instance_name):
    security_group_id = security_group()
    data = user_data()

    # Use default instance name
    if not instance_name:
        instance_name = 'captain-hook'

    try: 
        instance = ec2.create_instances(
            ImageId='ami-acd005d5',
            KeyName=key,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            UserData=data,
            SecurityGroupIds=[security_group_id],
            Placement={
                'AvailabilityZone': 'eu-west-1a'
            },
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        }
                    ]
                }
            ]
        )
        
        # Wait for instance to start up before returning
        instance = instance[0]        
        while instance.state['Name'] != 'running':
            print ('Instance is starting up...')
            time.sleep(10)
            instance.reload()

        print ('Instance created with id:', instance.id)
        return instance
    except Exception as e:
        print ('Error while creating instance:', str(e))
        sys.exit(1)

def main():
    create_instance(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()