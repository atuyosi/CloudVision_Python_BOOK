#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from google.cloud import storage
from google.protobuf import json_format
from google.cloud import vision as vision

from google.cloud.vision import enums
from google.cloud.vision import types

import pathlib

# サンプルコードのディレクトリから画像のあるディレクトリへのパスを解決する
image_dir = pathlib.Path(__file__).parent.parent.resolve() / 'image_data'

features = [
            types.Feature(type=enums.Feature.Type.DOCUMENT_TEXT_DETECTION),]

requests = []

client = vision.ImageAnnotatorClient()

image_files = list(image_dir.glob('test_jpn_*.jpg'))


# image_files = ['test_jpn_01.jpg', 'test_jpn_02.jpg', 'test_jpn_03.jpg']

for filename in image_files :
    with open(filename, 'rb') as image_file:
            image = types.Image(content = image_file.read())
        # image = types.Image(source= '')
        
    request = types.AnnotateImageRequest(image=image, features=features)
    requests.append(request)

response = client.batch_annotate_images(requests)

for rp in response.responses:
       print(rp.text_annotations[0].description)

