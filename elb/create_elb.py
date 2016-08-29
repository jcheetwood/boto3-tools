import boto3

print("***This script is for creating a new Load Balancer in AWS for the currently configured region. To change regions please use aws configure command to set region.***")

elb_name = input("Enter Load Balancer Name: ")
print(elb_name)

elb_protocol = input("Enter the Protocol the Load Balancer will handle: ")
print(elb_protocol)

elb_port = input("Enter the port the Load Balancer should listen on: ")
print(elb_port)

instance_protocol = input("Enter the protocol to forward to the Instance: ")
print(instance_protocol)

instance_port = input("Enter the port of the Instance to forward to: ")
print(instance_port)

#elb_avail_zone = input("Enter the availability zone you want the Load Balancer in: ")
#print(elb_avail_zone)

elb_subnets = input("Enter the subnets you want the Load Balancer to cover: ")
print(elb_subnets)

elb_security_grp = input("Enter the security group id you want the Load Balancer to join: ")
print(elb_security_grp)

client = boto3.client('elb')

response = client.create_load_balancer(
    LoadBalancerName=elb_name,
    Listeners=[
        {
            'Protocol': elb_protocol,
            'LoadBalancerPort': int(elb_port),
            'InstanceProtocol': instance_protocol,
            'InstancePort': int(instance_port),
        },
    ],
#    AvailabilityZones=[
#        elb_avail_zone,
#    ],
    Subnets=[
        elb_subnets,
    ],
    SecurityGroups=[
        elb_security_grp,
    ],
)

print(response)
