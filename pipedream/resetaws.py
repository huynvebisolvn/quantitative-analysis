import boto3

#Cron Expression: 55 0/2 * * *
def start(instance_id):
    instances = conn.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    for instance in instances:
        if (instance.id == instance_id):
            instance.start()

def stop(instance_id):
    instances = conn.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        if (instance.id == instance_id):
            instance.stop()

access_key = "xxx"
secret_key = "xxx"
region = "eu-west-1"
conn = boto3.resource('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)

def handler(pd: "pipedream"):
    time_flg = pd.steps["trigger"]["event"]["timezone_utc"]["time"]["minute"]
    if (time_flg == 3):
        stop('i-0bc6ba11f82c2bf66')
        print("stop")
    if (time_flg == 55):
        start('i-0bc6ba11f82c2bf66')
        print("start")
    print(time_flg)
    return {"code": 200}
