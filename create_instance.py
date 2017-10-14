#!/usr/bin/python3
# To do: AWS profiles
# To do: Implement usability 

import boto3

boto3.setup_default_session(profile_name='boto3')
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
        error = str(e)
        print ('Cannot read user data:', error)

# Configure security group
def security_group():
    group_name = 'http_ssh'
    group_desc = 'Allow incoming http and ssh traffic'

    # If security group exists, get group id
    groups = [sg.group_name for sg in ec2.security_groups.all()]

    if group_name in groups:
        response = client.describe_security_groups(GroupNames = [group_name])
        group_id = response['SecurityGroups'][0]['GroupId']
        return group_id
    # Otherwise, create security group
    else: 
        try:
            response = ec2.create_security_group(
                GroupName=group_name,
                Description=group_desc
            )
            security_group_id = response['GroupId']
            print ('Security Group %s created with id %s' % (security_group_id))

            data = ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
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
            print ('Ingress Successfully Set %s' % data)
            return security_group_id
        except Exception as e:
            error = str(e)
            print ('Error occurred while creating security group:', error)

# Create the instance
def create_instance():
    security_group_id = security_group()
    data = user_data()

    instance = ec2.create_instances(
        ImageId='ami-acd005d5',
        KeyName='nginx_instance_keypair', # Create key pair? Import key pair?
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
                        'Value': 'captain-hooks'
                    }
                ]
            }
        ]
    )

    print ('Instance created with id:', instance[0].id)

def main():
    create_instance()

if __name__ == '__main__':
  main()