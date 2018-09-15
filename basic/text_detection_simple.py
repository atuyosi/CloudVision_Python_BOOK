#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from google.cloud import storage
from google.protobuf import json_format
from google.cloud import vision as vision

import pathlib

image_dir = pathlib.Path(__file__).parent.parent.resolve() / 'image_data'

filename = str(image_dir / 'sample.jpg')

client = vision.ImageAnnotatorClient()
response = client.text_detection(image=open(filename,'rb'))

if response.error.code == 0 :
    print(response.text_annotations[0].description)
else:
    print("Error code: {}".format(response.error.code))
