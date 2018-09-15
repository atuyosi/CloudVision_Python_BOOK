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

filename = str(image_dir / 'sample.jpg')

client = vision.ImageAnnotatorClient()

    
image = vision.types.Image()


image.content = open(filename,'rb').read()

image_context = vision.types.ImageContext(language_hints = ['en'])

request = types.AnnotateImageRequest(image = image ,
                features= [{'type': vision.enums.Feature.Type.TEXT_DETECTION}],
                    image_context = vision.types.ImageContext(language_hints = ['en']))


response_from_url = client.annotate_image(request)


print(response_from_url)
