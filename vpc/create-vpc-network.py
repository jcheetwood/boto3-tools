import boto3

#--------------------------------------------------------------------------------------------------------------------
#This script can be used to create a VPC network in a specified region in AWS.
#It will also name the VPC, create and name subnets, 
#

#--------------------------------------------------------------------------------------------------------------------
#Set Region to work in
#--------------------------------------------------------------------------------------------------------------------
region = input("Enter the region you wish to work in: (ie. us-west-2, eu-central-1, eu-west-1) ")

#--------------------------------------------------------------------------------------------------------------------
#Set CiDR Block for VPC
#--------------------------------------------------------------------------------------------------------------------
cidr_blk = input("Enter the CiDR block (IP Block) of the VPC you are trying to create: (ie. 10.0.0.0/16) ")

#--------------------------------------------------------------------------------------------------------------------
#Split cidr block for subnet creation
#--------------------------------------------------------------------------------------------------------------------
cidr_list = cidr_blk.split(".")

#--------------------------------------------------------------------------------------------------------------------
#Print Split List
#--------------------------------------------------------------------------------------------------------------------
print(cidr_list)

#--------------------------------------------------------------------------------------------------------------------
#Set VPC Name
#--------------------------------------------------------------------------------------------------------------------
vpc_name = input("Enter the a name for the VPC: ")

#--------------------------------------------------------------------------------------------------------------------
#Set number of subnets to create
#--------------------------------------------------------------------------------------------------------------------
num_subnets = input("Enter number of subnets you want the VPC to contain: ")

#--------------------------------------------------------------------------------------------------------------------
#Declare Session Region
#--------------------------------------------------------------------------------------------------------------------
client = boto3.setup_default_session(region_name=region)

#--------------------------------------------------------------------------------------------------------------------
#Declare Boto Service being used
#--------------------------------------------------------------------------------------------------------------------
client = boto3.client('ec2')

#--------------------------------------------------------------------------------------------------------------------
#Create VPC
#--------------------------------------------------------------------------------------------------------------------
print("**Creating VPC Network**")
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
print("**VPC Network Successfully Created**")
#--------------------------------------------------------------------------------------------------------------------
#Internet Gateway
#--------------------------------------------------------------------------------------------------------------------
print("**Creating Internet Gateway**")
create_igw = client.create_internet_gateway(
)

igw = create_igw['InternetGateway']['InternetGatewayId']
print("**Internet Gateway Successully Created: " + str(igw) + " **")

#--------------------------------------------------------------------------------------------------------------------
#Attach Internet Gateway
#--------------------------------------------------------------------------------------------------------------------
print("Attaching Internet Gateway to VPC")
attach_igw = client.attach_internet_gateway(
    InternetGatewayId=igw,
    VpcId=vpc_id
)

print("**Internet Gateway Successfully Attached**")

#--------------------------------------------------------------------------------------------------------------------
#Get VPC Route Table
#--------------------------------------------------------------------------------------------------------------------
print("**Now Querying VPC Route Table**")
get_route_table = client.describe_route_tables(
    Filters=[
        {
            'Name': 'vpc-id',
            'Values': [
                vpc_id,
            ]
        },
    ]
)

#--------------------------------------------------------------------------------------------------------------------
#Set Route Table Variables for subnet association
#--------------------------------------------------------------------------------------------------------------------
route_table_id = get_route_table['RouteTables'][0]['RouteTableId']
print("**Route Table Located Successfully: " + str(route_table_id) + " **")

#--------------------------------------------------------------------------------------------------------------------
#Set Route Table Name
#--------------------------------------------------------------------------------------------------------------------
print("**Naming Route Table after VPC**")
create_name_tag = client.create_tags(
    Resources=[
        route_table_id,
    ],
    Tags=[
        {
            'Key': 'Name',
            'Value': str(vpc_name) + "-route-tbl"
        },
    ]
)
print("**Route Table Named Successfully**")

#--------------------------------------------------------------------------------------------------------------------
#Create Default Internet Route
#--------------------------------------------------------------------------------------------------------------------
print("**Creating Default Route to the Internet**")

create_route = client.create_route(
    RouteTableId=route_table_id,
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=igw,
)

print("**Default Route Created**")

#--------------------------------------------------------------------------------------------------------------------
#Create Subnets
#--------------------------------------------------------------------------------------------------------------------
print("Creating Subnets: ")
for i in range(0, int(num_subnets)):

    #Set Each Subnets Name
    subnet_name = input("Enter Subnet Name: ")

    #Creates Each Subnet
    response = client.create_subnet(
        VpcId=vpc_id,
        CidrBlock=str(cidr_list[0]) + "." + str(cidr_list[1]) + "." + str(int(cidr_list[2]) + int(i)) + ".0/24",
        AvailabilityZone=str(region) + str('a')
    )

    #Returns the Subnet ID
    print(response['Subnet']['SubnetId'])

    #Set Subnet ID for Route Table Association and Naming
    subnet_id = response['Subnet']['SubnetId']

    #Set Subnets Route Table
    associate_route_table = client.associate_route_table(
        SubnetId=subnet_id,
        RouteTableId=route_table_id
    )

    #Set Subnet Name
    create_subnet_name = client.create_tags(
        Resources=[
            subnet_id,
        ],
        Tags=[
            {
                'Key': 'Name',
                'Value': subnet_name
            },
        ]
    )
    print(create_subnet_name)

print("Subnets Successfully Created!")
print("VPC Network Creation - Successful")
