import boto3



def list_regions():
    desc_regions = client.describe_regions(
    )
    i = 0
    for region in desc_regions['Regions']:
        i += 1
        print(str(i) + ". " + region['RegionName'])
    selected_region = input("Enter the number of the region you wish to access: ")
    return desc_regions['Regions'][int(selected_region) - 1]['RegionName']

def list_vpcs():
    response = client.describe_vpcs()
    print(response)



region = list_regions()
client = boto3.client('ec2')
list_vpcs()