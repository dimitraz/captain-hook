yum -y update && yum -y upgrade
yum install -y python36
yum install -y docker
service docker start
usermod -a -G docker ec2-user