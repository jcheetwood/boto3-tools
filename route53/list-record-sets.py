"""
HOSTED ZONE ID will need to replaced with AWS values.
"""

import boto3

client = boto3.client('route53')

record_set = client.list_resource_record_sets(
    HostedZoneId='HOSTEd ZONE ID',
)



def print_dns_records():
    for index,i in enumerate(record_set['ResourceRecordSets']):
        print("\n")
        print(str(index +1) + ": " + record_set['ResourceRecordSets'][index]['Name'])
        a = index
        if record_set['ResourceRecordSets'][a].get('ResourceRecords', None):
            for index1,n in enumerate(record_set['ResourceRecordSets'][a]['ResourceRecords']):
                print("    " + record_set['ResourceRecordSets'][a]['ResourceRecords'][index1]['Value'])
        else:
             print("    " + record_set['ResourceRecordSets'][a]['AliasTarget']['DNSName'])

print_dns_records()

