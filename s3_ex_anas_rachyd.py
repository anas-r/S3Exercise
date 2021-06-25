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

# METHODES "HELPER"
def check_file_in_bucket(file, bucket):
    '''
    Retourne True si le fichier existe dans le bucket, False sinon.
    
    :param str file: nom de fichier.
    :param obj bucket: object de type bucket.

    '''
    file_md5 = md5(open(os.path.join(folder_path,file), 'rb').read()).hexdigest()
    if bucket is not None:
        for obj in bucket:
            obj_md5 = obj.get('ETag')[1:-1]
            if file_md5 == obj_md5:
                return True
    return False

def check_obj_in_folder(obj, folder_path):
    '''
    Retourne True si le fichier existe dans le dossier, False sinon.
    
    :param obj obj: objet contenu dans un bucket.
    :param str folder_path: chemin complet vers le dossier.
    
    '''
    obj_md5 = obj.get('ETag')[1:-1]
    folder_files = get_first_level_files(folder_path)
    for file in folder_files:
        file_md5 = md5(open(os.path.join(folder_path,file), 'rb').read()).hexdigest()
        if file_md5 == obj_md5:
            return True
    return False

def get_first_level_files(folder_path):
    '''
    Retourne une liste des nom des fichiers au premier niveau contenus dans un dossier.
    N'explore pas les sous-dossiers.
    
    :param str folder_path: chemin complet vers le dossier.
    
    '''
    folder_files = []
    # on extrait les noms de fichiers dans le dossier
    for (_, _, files) in os.walk(folder_path):
        for name in files:
            folder_files.append(name)
        break
    return folder_files

# METHODES PRINCIPALES
def upload_to_bucket(folder_path, bucket_name):
    '''
    Upload des fichiers qui n'existent pas dans le bucket.
    
    :param str folder_path: chemin complet vers le dossier.
    :param str bucket_name: nom du bucket.
    '''
    folder_files = get_first_level_files(folder_path)
    bucket = s3.list_objects(Bucket=bucket_name).get('Contents')

    for file in folder_files:
        if not (check_file_in_bucket(file, bucket)):
            try:
                s3.upload_file(os.path.join(folder_path,file), bucket_name, file)
                print("Uploaded file: {0}".format(file))
            except ClientError as e:
                logging.error(e)
                
def delete_unnexisting_files(folder_path, bucket_name):
    '''
    Supprime du bucket des fichiers qui n'existent pas dans le dossier local.
    
    :param str folder_path: chemin complet vers le dossier.
    :param str bucket_name: nom du bucket.
    '''
    bucket = s3.list_objects(Bucket=bucket_name).get('Contents')

    if bucket is not None:
        for obj in bucket:
            if not (check_obj_in_folder(obj, folder_path)):
                try:
                    obj_key = obj.get('Key')
                    s3.delete_object(Bucket=bucket_name, Key=obj_key)
                    print("Deleted file: {0}".format(obj_key))
                except ClientError as e:
                    logging.error(e)

buckets = s3.list_objects(Bucket='testo').get('Contents')

if __name__ == '__main__':
    if not os.path.isdir(sys.argv[1]):
        print("Répertoire invalide.")
    else:
        folder_path = sys.argv[1]
        bucket_name = sys.argv[2]
        try:
            print('Syncing "{0}" with "{1}"'.format(bucket_name, folder_path),end="\n")
            bucket = s3.list_objects(Bucket=sys.argv[2])
            upload_to_bucket(folder_path, bucket_name)
            delete_unnexisting_files(folder_path, bucket_name)
            print("Sync complete.")
        except ClientError as e:
            logging.log(e)
