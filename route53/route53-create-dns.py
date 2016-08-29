"""
HOST ZONE ID and DNS NAME and IP Value will need to replaced with AWS values.
"""

import boto3

client = boto3.client("route53")


dns_action = client.change_resource_record_sets(
    HostedZoneId='HOSTED ZONE ID',
    ChangeBatch={
        'Changes': [
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': 'DNS NAME',
                    'Type': 'A',
                    'TTL': 300,
                    'ResourceRecords': [
                        {
                            'Value': 'IP VALUE'
                        },
                    ],
                }
            },
        ]
    }
)
print(dns_action)