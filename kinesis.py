import json
import boto3
import os
from datetime import datetime, timedelta

#Send the json objects created in #1 to kinesis firehose so that they are processed and written to S3 

session = boto3.Session(aws_access_key_id="AKIA2OLGZXFFDIN7ZVV5",aws_secret_access_key="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",region_name="ap-south-1")

def lambda_handler(event, context):
    firehoseClient = session.client('firehose')
    resource = session.resource('iam')
    client = session.client('iam')
    list_of_objects = []
    for user in resource.users.all():
        Metadata = client.list_access_keys(UserName = user.user_name)
        LastUserUsed = user.password_last_used
        if Metadata['AccessKeyMetadata'] :
            list_of_keys = []
            for key in user.access_keys.all():
                AccessKeyId = key.access_key_id
                if(client.get_access_key_last_used(AccessKeyId=AccessKeyId)['AccessKeyLastUsed']['ServiceName'] == "N/A"):
                    LastUsedAccessKey = "N/A"
                    list_of_keys.append({"Access_key_id":AccessKeyId,"LastUsedAccessKey":LastUsedAccessKey,"SinceLastUsedAccessKey": SinceLastUsedAccessKeyDays})
            
                else:
                    LastUsedAccessKey = client.get_access_key_last_used(AccessKeyId=AccessKeyId)['AccessKeyLastUsed']['LastUsedDate']   
                    lastActivity = datetime.now(LastUsedAccessKey.tzinfo) - LastUsedAccessKey          
                    SinceLastUsedAccessKeyDays = lastActivity.days
                    list_of_keys.append({"Access_key_id":AccessKeyId,"LastUsedAccessKey":LastUsedAccessKey.strftime("%d/%m/%Y %H:%M:%S"),"SinceLastUsedAccessKey": SinceLastUsedAccessKeyDays})
            list_of_objects.append({"UserName":user.user_name,"Access_Keys": list_of_keys})
        else:
            print("User don`t have AccessKey")     
    
    print(list_of_objects)  
    
    for observation in list_of_objects:
        print("Observation ====>",observation)
