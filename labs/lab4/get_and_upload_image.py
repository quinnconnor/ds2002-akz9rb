import requests
import os
import logging
import boto3
from botocore.exceptions import ClientError

def download_file(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded to {file_path}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading: {e}")

def upload_file(local_file, bucket):
    s3 = boto3.client('s3')
    s3.put_object(
        Body = local_file,
        Bucket = bucket,
        Key = local_file,
        ACL='public-read'
    )
    print(f"File uploaded to s3://{bucket}/{local_file}")
    print(f"Found at: https://s3.amazonaws.com/{bucket}/{local_file}/")

def create_presigned_url(bucket_name, object_name, expiration=3600):
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

#get user input
image_url = input("Enter an image URL: ")
file_name = input("Enter file name to save as: ")
bucket = input("Enter s3 bucket name: ")
expiration = int(input("Enter expiration time for the URL in seconds: "))

#might need file path here
local_file = os.path.join(os.getcwd(), file_name)

#download file
download_file(image_url, local_file)

#upload file
upload_file(local_file, bucket)

presigned_url = create_presigned_url(bucket, local_file, expiration)

print(f"Presigned URL (for {expiration} seconds): {presigned_url}")
