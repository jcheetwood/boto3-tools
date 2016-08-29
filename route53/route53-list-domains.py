import boto3

client = boto3.client('route53domains')


response = client.list_domains(
)

print(response)