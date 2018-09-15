#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from google.cloud import storage
from google.protobuf import json_format
from google.cloud import vision_v1p3beta1 as vision
import pathlib

image_dir = pathlib.Path(__file__).parent.parent.resolve() / 'image_data'

filename = str(image_dir / 'handwritten.png')


client = vision.ImageAnnotatorClient()
image = vision.types.Image()

# image.source.image_uri = uri  # uri: The path to the file in Google Cloud Storage (gs://...)
image.content = open(filename, 'rb').read()

image_context = vision.types.ImageContext(
                language_hints=['en-t-i0-handwrit']
                #    language_hints=['mul-Latn-t-i0-handwrit']
                )

response_d = client.document_text_detection(image, image_context=image_context)

if response_d.error.code == 0 :
        print(response_d.text_annotations[0].description)
else:
        print("Error code: {}".format(response_d.error.code))
