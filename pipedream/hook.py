import boto3
import time

def public_ip_address(instance_id):
    instances = conn.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        if (instance.id == instance_id):
            return instance.public_ip_address
    return ''

access_key = "xxx"
secret_key = "xxx"
region = "eu-west-1"
conn = boto3.resource('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)

def handler(pd: "pipedream"):
    #print(pd.steps["trigger"]["context"]["id"])
    ip_address = public_ip_address('i-0bc6ba11f82c2bf66')
    if (ip_address == ''):
        for i in range(1,12):
            ip_address = public_ip_address('i-0bc6ba11f82c2bf66')
            if (ip_address != ''):
                break
            time.sleep(10)
    return {"ip": ip_address}

#POST: http://%7B%7Bsteps.python.%24return_value.ip%7D%7D/btc
