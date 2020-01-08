import gzip
import os
import boto3
import botocore
from datetime import datetime

s3 = boto3.client('s3', region_name='us-east-1')
sqs = boto3.client('sqs', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def send_message_to_queue(msg):
    
    queue_name = os.environ['QUEUE_NAME']

    queue_url = sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=msg)

    return response


def create_item(line):

    item = {}

    ## ORDER MATTERS
    cols = """member_id achievement_category#achievement_date#achievement_id achievement_id achievement_category
    achievement_ts_utc member_id-achievement_id etl_update_ts etl_source_cd achievement_date achievement_facility_id""".split()

    for col, value in zip(cols, line.decode().split('|')):
        if str(value).strip() != "":
            item[col] = str(value).strip()
    
    return item
    
def resend_if_more_files_remaining(file_names):
    
    if len(file_names) > 0:
        new_message = ','.join(file_names)
        send_message_to_queue(new_message)
        print(f'Message sent - {len(file_names)} files in new message')
    
    return None

def lambda_handler(event, context):

    bucket_name = os.environ['BUCKET_NAME']
    table_name = os.environ['TABLE_NAME']
    
    table = dynamodb.Table(table_name)

    for record in event['Records']:
        file_names = record['body'].split(',')
        key = file_names.pop()
        temp = '/tmp/' + key.replace('/', '-')
        
        try:
            s3.download_file(bucket_name, key, temp)
            print(f'Downloaded {key}')
        except botocore.exceptions.ClientError as e:
            print(f'{e.response} - {key}')
            return

        with table.batch_writer() as batch:
            with gzip.open(temp, 'rb') as data:
                starttime = datetime.now()
                lap_time = starttime
                for i, line in enumerate(data):
                    if i % 10000 == 0 and i > 0:
                        print(f'Records loaded: {i} - Total time: {datetime.now() - starttime} - Lap time: {datetime.now() - lap_time}')
                        lap_time = datetime.now()
                    item = create_item(line)
                    batch.put_item(Item=item)
        print(f'Success loaded Batch File - {key}')

        resend_if_more_files_remaining(file_names)
        
