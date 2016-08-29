#Import Library
import boto3

#Set Boto3 client
client = boto3.client('route53')

#Query for DNS names
response = client.list_hosted_zones_by_name(
)

#Print Each of the domain names
def print_domains():
    for index,i in enumerate(response['HostedZones']):
    #while i < len(response['HostedZones']):
        dns_name = response['HostedZones'][index]['Name'][:-1]
        hosted_zone = response['HostedZones'][index]['Id'].replace("/hostedzone/","")
        print(str(index +1) + "." + dns_name + ", " + hosted_zone)

#Print each of the DNS Records for a given Domain
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

#Select whether to create, delete or update a record
def dns_choices():
    invalid_input = True
    print("\n")
    print("Please selection an action: ")
    print("1. Create New DNS Record")
    print("2. Update exisiting DNS Record")
    print('3. Delete DNS Record Set')
    user_selection = int(input("Selection: "))

    while invalid_input:

        #Handles Creating New DNS Records
        if user_selection == 1:
            print("You have selected to Create a new DNS Record")
            record_type = input("Input Record type: ie: 'SOA' | 'A' | 'TXT' | 'NS' | 'CNAME' | 'MX' | 'PTR' " +
                                "| 'SRV' |'SPF' | 'AAAA': ")
            record_name = input("Enter the record name you wish to create: ie: hostname.domain.whatever ")
            ip_addr = input("Enter the IP Address or CNAME of the record to create: ie: 10.0.0.0 ")
            invalid_input = False
            dns_action = client.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'CREATE',
                            'ResourceRecordSet': {
                                'Name': record_name,
                                'Type': record_type,
                                'TTL': 300,
                                'ResourceRecords': [
                                    {
                                        'Value': ip_addr
                                    },
                                ],
                            }
                        },
                    ]
                }
            )
            print(dns_action)

        #Handles DNS Changes
        elif user_selection == 2:

            print("You have selected to Update an existing DNS Record")

            #Print out each of the DNS Entries for the selected Domain
            print_dns_records()

            #User Selects Entry to Delete from Domain
            record_to_update = input("Enter the number of the DNS Record you wish to update: ")

            #Print Name of Entry Selected
            print(record_set['ResourceRecordSets'][int(record_to_update) - 1]['Name'])
            print(record_set['ResourceRecordSets'][int(record_to_update) - 1]['Type'])
            print(record_set['ResourceRecordSets'][int(record_to_update) - 1]['ResourceRecords'][0]['Value'])

            #Set Name, IP, Type from record_set dictionary for selected DNS record
            record_type = record_set['ResourceRecordSets'][int(record_to_update) - 1]['Type']
            record_name = record_set['ResourceRecordSets'][int(record_to_update) - 1]['Name']
#            ip_addr = record_set['ResourceRecordSets'][int(record_to_delete) - 1]['ResourceRecords'][0]['Value']
            ip_addr = input("Enter the updated IP Address or CNAME of the record you are updating: ")
            invalid_input = False
            dns_action = client.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                'Name': record_name,
                                'Type': record_type,
                                'TTL': 300,
                                'ResourceRecords': [
                                    {
                                        'Value': ip_addr
                                    },
                                ],
                            }
                        },
                    ]
                }
            )
            print(dns_action)

        #Handles DNS Deletes
        elif user_selection == 3:
            print("You have selected to Deleted a DNS Record")

            #Print out each of the DNS Entries for the selected Domain
            print_dns_records()

            #User Selects Entry to Delete from Domain
            record_to_delete = input("Enter the number of the DNS Record you wish to delete: ")

            #Print Name of Entry Selected
            print(record_set['ResourceRecordSets'][int(record_to_delete) - 1]['Name'])
            print(record_set['ResourceRecordSets'][int(record_to_delete) - 1]['Type'])
            print(record_set['ResourceRecordSets'][int(record_to_delete) - 1]['ResourceRecords'][0]['Value'])

            #Set Name, IP, Type from record_set dictionary for selected DNS record
            record_type = record_set['ResourceRecordSets'][int(record_to_delete) - 1]['Type']
            record_name = record_set['ResourceRecordSets'][int(record_to_delete) - 1]['Name']
            ip_addr = record_set['ResourceRecordSets'][int(record_to_delete) - 1]['ResourceRecords'][0]['Value']

            #End While loop
            invalid_input = False

            #Make DNS Delete Request to AWS
            dns_action = client.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'DELETE',
                            'ResourceRecordSet': {
                                'Name': record_name,
                                'Type': record_type,
                                'TTL': 300,
                                'ResourceRecords': [
                                    {
                                        'Value': ip_addr
                                    },
                                ],
                            }
                        },
                    ]
                }
            )
            print(dns_action)
        else:
            print("Please make a valid selection")
            user_selection = int(input("Selection: "))
            continue

# Print all the Domains
print_domains()

#Select Hosted Zone to Edit
selected_hosted_zone = input("Enter the number of the Domain you wish to edit: ")
zone_id = response['HostedZones'][int(selected_hosted_zone) - 1]['Id'].replace("/hostedzone/", "")

#Set record set
record_set = client.list_resource_record_sets(
    HostedZoneId=zone_id,
)

#Print DNS Edit Options
dns_choices()
