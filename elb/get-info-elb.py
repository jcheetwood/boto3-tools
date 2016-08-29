import boto3

client = boto3.client('elb')

print("This script outputs all the current load balancers in production for the given region you have set in aws configure.")

response = client.describe_load_balancers()

print(response.get('LoadBalancerDescriptions')[0]['LoadBalancerName'])