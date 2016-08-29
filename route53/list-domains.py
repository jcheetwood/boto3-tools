import boto3

client = boto3.client('route53')

response = client.list_hosted_zones(
)

print(response)