yum -y update && yum -y upgrade

yum install docker -y
service docker start
usermod -a -G docker ec2-user