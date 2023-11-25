import json
import boto3
import os

# Denne koden kan også kjøres som en selvstendig applikasjon (Uten SAM) bare gjøre følgende
# (dersom man har python på maskinen sin altså...)
#
# Instruksjoner for å kjøre ...
#
# pip3 install -r requirements.txt
# Open up template.yaml
# change the BucketName line 27 in template.yaml from kandidat-2030 to something you prefer if you want
# To set a local environment variable type: export BUCKET_NAME="kandidat-2030"
# to test the python code type: cd DevOps-Eksamen-2023/kjell/hello_world then type: python3 app.py
# to test the sam invoke type: cd DevOps-Eksamen-2023/kjell then type: sam local invoke HelloWorldFunction --event events/event.json
#
# Hilsen kandidat-2030 og Kjell

s3_client = boto3.client('s3', region_name='eu-west-1')
rekognition_client = boto3.client('rekognition', region_name='eu-west-1')

# Oppgave 1A
BUCKET_NAME = os.environ.get('BUCKET_NAME')
print("BUCKET_NAME:", BUCKET_NAME)

if BUCKET_NAME:
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
        print(f"Bucket '{BUCKET_NAME}' exists, now running the bucket.")
    except s3_client.exceptions.NoSuchBucket:
        print(f"Bucket '{BUCKET_NAME}' does not exist. You may want to create it before running your application.")
    except Exception as e:
        print(f"Error checking bucket '{BUCKET_NAME}': {str(e)}")

def lambda_handler(event, context):
    print("Environment Variables:", os.environ)
    BUCKET_NAME = os.environ.get('BUCKET_NAME')
    # Check if BUCKET_NAME is set
    if not BUCKET_NAME:
        return {
            "statusCode": 500,
            "body": "Environment variable BUCKET_NAME is not set."
        }
    
    # List all objects in the S3 bucket
    paginator = s3_client.get_paginator('list_objects_v2')
    rekognition_results = []  # Store the results

    for page in paginator.paginate(Bucket=BUCKET_NAME):
        for obj in page.get('Contents', []):
            # Perform PPE detection using Rekognition
            rekognition_response = rekognition_client.detect_protective_equipment(
                Image={
                    'S3Object': {
                        'Bucket': BUCKET_NAME,
                        'Name': obj['Key']
                    }
                },
                SummarizationAttributes={
                    'MinConfidence': 80,  # Confidence level threshold
                    'RequiredEquipmentTypes': ['FACE_COVER']
                }
            )
            rekognition_results.append(rekognition_response)

    return {
        "statusCode": 200,
        "body":  json.dumps(rekognition_results),
    }

print(lambda_handler(None, None))