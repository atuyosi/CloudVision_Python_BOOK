#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from google.cloud import storage

import re
import sys

import pathlib

gcs_destination_uri = "gs://[sample-bucket-name]/upload_test/"

filename = 'example.pdf'

storage_client = storage.Client()
blob_list = []

match = re.match(r'gs://([^/]+)/(.+)?', gcs_destination_uri)

if match :
        bucket_name = match[1]  # match.group(1)

    if match[2] :
                prefix = match[2].rstrip('/') # match.group(2)

else:
        print("Pattern not matched!")

try:
        bucket = storage_client.get_bucket(bucket_name=bucket_name)
    
    if match :
                blob = bucket.blob("{}/".format(prefix) + filename)
    else:
                blob = bucket.blob(filename)
    with open(filename, 'rb') as fp:
                blob.upload_from_file(fp)

except Exception as e:
        print(e)
    print('Sorry, that bucket does not exist!')
    sys.exit(-1)

print(blob.public_url)
