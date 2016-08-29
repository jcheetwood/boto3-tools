import boto3

client = boto3.client('elb')

print("This script is used to delete Load Balancers in AWS, be sure you have aws configure set to the correct region of the load balancer before running this script.")

elb_name = input("Enter the name of the Load Balancer you wish to delete: ")
print(elb_name)

response = client.delete_load_balancer(
    LoadBalancerName=elb_name
)

print(response)