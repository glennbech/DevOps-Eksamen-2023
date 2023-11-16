import json
import boto3
import os

# Denne koden kan også kjøres som en selvstendig applikasjon (Uten SAM) bare gjøre følgende
# (dersom man har python på maskinen sin altså...)
#
# Instruksjoner for å kjøre ... (Kan sikkert lage container senere ..)
#
# pip3 install -r requirements.txt
# export BUCKET_NAME=<you_bucket>
# echo $BUCKET_NAME
# python3 app.py
#
# Hilsen Kjell

s3_client = boto3.client('s3', region_name='eu-west-1')
rekognition_client = boto3.client('rekognition', region_name='eu-west-1')

# Oppgave 1A
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'default_bucket_name')


def create_s3_bucket(bucket_name):
    try:
        location_constraint = s3_client.meta.region_name  # Use the current region
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': location_constraint}
        )
        print(f"Bucket '{bucket_name}' created successfully.")
    except s3_client.exceptions.BucketAlreadyOwnedByYou as e:
        print(f"Bucket '{bucket_name}' already exists.")
    except Exception as e:
        print(f"Error creating bucket '{bucket_name}': {str(e)}")


def lambda_handler(event, context):
    
    
    # Create S3 bucket if it doesn't exist
    create_s3_bucket(BUCKET_NAME)


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