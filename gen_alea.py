import logging
import os
import sys
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from hashlib import md5
from binascii import hexlify
from config import ENDPOINT_URL, KEY_ID, ACCESS_KEY

s3 = boto3.client('s3',
                endpoint_url=ENDPOINT_URL,
                aws_access_key_id=KEY_ID,
                aws_secret_access_key=ACCESS_KEY,
                config=Config(signature_version='s3v4'),
                region_name='us-east-1')

def upload_file_to_bucket(file, bucket_name):
    print("Uploaded file: {0}".format(file))
    s3.upload_file(file, bucket_name, file)

if __name__ == '__main__':
    # création
    for i in range(20):
        f = open(os.path.join(os.getcwd(),'random','random-{}'.format(i)), 'wb')
        f.write(os.urandom(1000))
        s3.upload_file(os.path.join(os.getcwd(),'random','random-{}'.format(i)), sys.argv[1], 'random-{}'.format(i))
        f.close()
    # modification
    for i in range(10):
        f = open(os.path.join(os.getcwd(),'random','random-{}'.format(i)), 'wb')
        f.write(os.urandom(1000))
        f.close()
    # fichiers qui n'existent que dans le local
    for i in range(10):
        f = open(os.path.join(os.getcwd(),'random','randomX-{}'.format(i)), 'wb')
        f.write(os.urandom(1000))
        f.close()
    
    