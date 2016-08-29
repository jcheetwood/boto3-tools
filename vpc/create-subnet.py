"""
VpcId and AvailabilityZone need to be replaced with AWS values for your environment.
"""

import boto3

#Set Region to work in
region = input("Enter the region you wish to work in: (ie. us-west-2, eu-central-1, eu-west-1) ")

#Set CiDR Block for VPC
cidr_blk = input("Enter the CiDR block (IP Block) of the Subnet you are trying to create: (ie. 10.0.0.0/16) ")

#Declare Session Region
aws_region = boto3.setup_default_session(region_name=region)

#Set boto3 client
client = boto3.client('ec2')

#Create Subnet VPC
response = client.create_subnet(
    VpcId='VpcId',
    CidrBlock=cidr_blk,
    AvailabilityZone='AvailabilityZone'
)

print(response)