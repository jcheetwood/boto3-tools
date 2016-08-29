import boto3

#Set Region to work in
region = input("Enter the region you wish to work in: (ie. us-west-2, eu-central-1, eu-west-1) ")

#Set CiDR Block for VPC
cidr_blk = input("Enter the CiDR block (IP Block) of the VPC you are trying to create: (ie. 10.0.0.0/16) ")

#Set VPC Name
vpc_name = input("Enter the a name for the VPC: ")

#Declare Session Region
client = boto3.setup_default_session(region_name=region)

#Declare Boto Service being used
client = boto3.client('ec2')

#Create VPC
response = client.create_vpc(
    CidrBlock=cidr_blk,
    InstanceTenancy='default'
)

print(response['Vpc']['VpcId'])

vpc_id=response['Vpc']['VpcId']

create_name_tag = client.create_tags(
    Resources=[
        vpc_id,
    ],
    Tags=[
        {
            'Key': 'Name',
            'Value': vpc_name
        },
    ]
)

print(create_name_tag)