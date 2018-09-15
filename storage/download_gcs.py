#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from google.cloud import storage
from google.protobuf import json_format

import sys
import re


gcs_destination_uri = "gs://[sample-bucket-name]/output/"

blob_list = []

match = re.match(r'gs://([^/]+)/(.+)?', gcs_destination_uri)

# Cloud Storageにアクセスするクライアントの初期化
storage_client = storage.Client()

if match :
    bucket_name = match[1]  # match.group(1)
    prefix = match[2] # match.group(2)
    
    bucket = storage_client.get_bucket(bucket_name=bucket_name)

else:
    print("URI Pattern not matched!", file=sys.stderr)
    

# filelのリストを取得
blob_list = list(bucket.list_blobs(prefix=prefix))


# 各ファイルへのアクセス
for gcs_obj in blob_list :
    print(type(gcs_obj))
    json_string = gcs_obj.download_as_string()
    
    # json_format.Parse()を使用すると、通常のPython用ライブラリと同じ形式のオブジェクトとして扱える
    response = json_format.Parse(json_string, vision.types.AnnotateFileResponse())

    for response in response.responses :    
    
    
        annotation = response.full_text_annotation
    
        print(type(annotation))
