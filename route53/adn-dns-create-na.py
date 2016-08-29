"""
HOST ZONE ID and DNS NAME will need to replaced with AWS values.
"""

import boto3

client = boto3.client('route53')



na_countries = ["AI","AG", "AW", "BB", "BM", "BZ", "BQ", "BS", "CR", "CU", "CW", "DM", "DO", "GD", "GL", "GP", "GT", "HT", "HN", "JM", "KN", "MX", "MQ", "MS", "NI", "PA", "PR", "SV", "SX", "TC", "TT", "UM"]



for i in na_countries:
    try:
        response = client.change_resource_record_sets(
            HostedZoneId='HOSTED ZONE ID',
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': 'DNS NAME',
                            'Type': 'A',
                            'SetIdentifier': i,
                            'GeoLocation': {
                                'CountryCode': i,
                            },
                            'AliasTarget': {
                                'HostedZoneId': 'HOSTED ZONE ID',
                                'DNSName': 'DNS NAME',
                                'EvaluateTargetHealth': False
                            },
                        }
                    },
                ]
            }
        )
    except:
        print("Record Exists Already.")