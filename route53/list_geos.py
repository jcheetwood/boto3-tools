import boto3

client = boto3.client('route53')

response = client.list_geo_locations(
    StartCountryCode='*',
)

print(response)