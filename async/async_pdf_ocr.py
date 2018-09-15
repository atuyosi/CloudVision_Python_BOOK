#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from google.cloud import storage
from google.cloud import vision as vision
from google.protobuf import json_format
from google.rpc import code_pb2 as code

from time import sleep
import sys
import re

import argparse

import pathlib

def async_ocr_on_gcs(gcs_source_uri, gcs_destination_uri):
    """非同期でGCS上のPDFから文字認識する"""

    client = vision.ImageAnnotatorClient()
    feature = vision.types.Feature(type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)

    batch_size = 5

    mime_type_pdf = 'application/pdf'
    mime_type_tiff = 'image/tiff'


    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)

    # ファイルの拡張子でMIME TYPEを切り替える
    if gcs_source_uri.endswith('.pdf'):
        mime_type = mime_type_pdf
    elif gcs_source_uri.endswith('.tiff'):
        mime_type = mime_type_tiff
    else:
        mime_type = None

    # InputConfigおよびOutputConfigクラスのインスタンスを初期化
    input_config = vision.types.InputConfig(gcs_source=gcs_source, mime_type=mime_type)
    output_config = vision.types.OutputConfig(gcs_destination=gcs_destination, batch_size=batch_size)


    # AsyncAnnotateFileRequest の初期化
    async_request = vision.types.AsyncAnnotateFileRequest(features=[feature], input_config=input_config, output_config=output_config)


    # async_batch_annotate_files()メソッドの呼び出し
    # 戻り値は`google.api_core.operation.Operation`クラスのインスタンス
    try:
        task = client.async_batch_annotate_files(requests=[async_request])
    except Exception as e:
        print(e)
        if task.operation.error .code > 0:
            print(task.operation.response)
            exit(-1)
        

    print(type(task))
    print(type(task.operation))


    print("Operation started: {}".format(task.operation))

    while (True):
        if task.done():
            # タスク完了
            print("Operation finished.")
            
            # google.cloud.vision.v1.OperationMetadata
            print(task.operation.metadata)

            if task.operation.error.code != code.OK :
                # エラーが起きたとき
                print("Error occured: {}".format(task.operation.error.code))
                print(task.operation.error.message)
            else:
                # 正常終了
                #print(type(task.operation.response))
                print("Recoginition task complete. Status: {}".format(task.operation.error.code))
                
                # google.cloud.vision.v1.AsyncBatchAnnotateFilesResponse
                print(task.operation.response) 

            break
        else:
            
            sleep(15)

def upload_to_gcs(filename, gcs_destination_uri):
    """fileをCloud Storageにアップロードするスクリプト"""

    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)?', gcs_destination_uri)

    if match :
        bucket_name = match[1]  # match.group(1)

        if match[2] :
            prefix = match[2].rstrip('/') # match.group(2)
        
    else:
        print("Pattern not matched!", file=sys.stderr)
        return None

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
        print('Error, that bucket does not exist!', file=sys.stderr)
        sys.exit(-1)

    return blob.public_url


if __name__ == "__main__" :

    # パーサーオブジェクトの初期化
    parser = argparse.ArgumentParser()

    parser.add_argument("filename", type=str, help="filename for text recognition")

    parser.add_argument('-u', '--upload', type=str, help="gcs-uri to upload" )
    parser.add_argument('-o', '--output', nargs='?',type=str, help="gcs-uri for output")

    args = parser.parse_args()

    filename = args.filename

    check_format = re.match(r'gs://[^/]+', args.upload)
    if check_format:
        gcs_source_uri = args.upload 
    else:
        print('Error, specified url is invalid!', file=sys.stderr)
        print("gcs_source_uri: {}".format(args.upload))
        sys.exit(-1)


    # ファイルのアップロード
    temp_url = upload_to_gcs(filename, gcs_source_uri)
    
    md = re.match(r'https://[^/]+/([^/]+)/(.+)?', temp_url)

    if md :
        gcs_source_uri = "gs://{0}/{1}".format(md[1], md[2])
    else:
        print('Error, upload file failed!', file=sys.stderr)
        sys.exit(-1)
    
    if args.output :
        gcs_destination_uri = args.output
    else:
        gcs_destination_uri = "gs://[sample-bucket-name]/output/"

    async_ocr_on_gcs(gcs_source_uri, gcs_destination_uri)