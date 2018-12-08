import json
import boto3
import data_index
import time

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    print(event)
    label_list=[]
    
    for record in event['Records']:
        PHOTO_BUCKET = record['s3']['bucket']['name']
        FILE_NAME = record['s3']['object']['key']

    print('reading image: {} from s3 bucket {}'.format(FILE_NAME, PHOTO_BUCKET))
    client = boto3.client('rekognition')
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': PHOTO_BUCKET,
                'Name': FILE_NAME
            }
        },
        MaxLabels=12,
        MinConfidence=80,
    )
    
    print('Detected labels for ' + FILE_NAME)
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
        label_list.append(label['Name'])
    
    ts = time.gmtime()
    created_time = time.strftime("%Y-%m-%dT%H:%M:%S", ts)
    print('Image created at {}....'.format(created_time))
    
    image_object = {
        'objectKey':FILE_NAME,
        'bucket':PHOTO_BUCKET,
        'createdTimestamp':created_time,
        'labels':label_list
    }
    
    es = data_index.connect_to_elastic_search()
    es.index(index="photos", doc_type="_doc", id=created_time, body=image_object)

    response = es.get(index="photos", doc_type="_doc", id=created_time)
   
    return response