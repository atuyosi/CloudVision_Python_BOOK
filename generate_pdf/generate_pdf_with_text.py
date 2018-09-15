#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
# from reportlab.rl_config import defaultPageSize
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.colors import red,black
from reportlab.lib.units import cm

# Pillow
from PIL import Image, ImageSequence

# PDFを画像化するモジュール
from pdf2image import convert_from_path, convert_from_bytes
import tempfile

from pathlib import Path

# ナチュラルソート
from natsort import natsorted
import math

# Cloud Storage bucketへのアクセス
from google.cloud import storage

# jsonからの変換
from google.cloud import vision as vision
from google.protobuf import json_format

# ファイルのパスの解決
import pathlib

import argparse

import sys
import re
import io

class PdfConfig:

    title = "No title"
    author = ""
    subject = ""
    
    default_fontname = "HeiseiKakuGo-W5"
    image_resolution = 300
    jpeg_quality = 95
    font_adjustment = 0.85
    image_embeded = True

    def __init__(self):
        pass
    

def get_data_from_gcs(gcs_uri):

    storage_client = storage.Client()
    blob_list = []
    response_list = []


    match = re.match(r'gs://([^/]+)/(.+)', gcs_uri)

    if match :
        bucket_name = match[1]  # match.group(1)
        prefix = match[2] # match.group(2)
    
        bucket = storage_client.get_bucket(bucket_name=bucket_name)
    else:
        print("Pattern not matched! Invalid gcs-uri.")
        return None

    # fileのリストを取得
    blob_list = natsorted(bucket.list_blobs(prefix=prefix), key=lambda x: x.name)

    for gcs_obj in blob_list :
        #print(type(gcs_obj))
        json_string = gcs_obj.download_as_string()
    
        # json_format.Parse()を使用すると、通常のPython用ライブラリと同じ形式のオブジェクトとして扱える
        temp_response = json_format.Parse(json_string, vision.types.AnnotateFileResponse())

        for res in  temp_response.responses :
            print(type(res))
            response_list.append(res)

    return response_list
    

def convert_pdf_to_img(pdf_filename, dpi=300):

    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(pdf_filename, dpi=dpi, output_folder=path)
    return images

def divide_tiff_image(tiff_filename):
    '''TIFFファイルを1ページずつ分割するメソッド'''

    images = []
    img = Image.open(tiff_filename)
        
    for page in ImageSequence.Iterator(img):
        im_buffer = io.BytesIO()
        page.save(im_buffer, format="png")
        images.append(Image.open(im_buffer))

    return images
      

def create_pdf(source_image_file, ta_pages, config, output_filename ):
    """透明なテキストと画像入りのPDFを作成するメソッド"""


    print("processing pdf: {0}".format(output_filename))

    is_normalized = False

    # PDFまたは画像をページ分割
    if re.search(r'\.pdf$', source_image_file ) :
        images = convert_pdf_to_img(source_image_file, dpi=config.image_resolution)
        is_normalized = True

    elif re.search(r'\.tiff$', source_image_file) :
        images = divide_tiff_image(source_image_file)
    else:
        print("Non-support file type. Existed!", file=sys.stderr)
        sys.exit(-1)

    newPdfPage = canvas.Canvas(output_filename)
    newPdfPage.setPageSize(A4)

    newPdfPage.saveState() # 念の為

    newPdfPage.setAuthor(config.author)
    newPdfPage.setTitle(config.title)
    newPdfPage.setSubject(config.subject)

    # 日本語用のフォントの登録（language packに含まれるもの）
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))

    # tiff file, PDF
    for i, image in enumerate(images):
        print(f"start page: {i}")

        print("image size: {}".format(image.size))
        image_width , image_height = image.size

        ratio = image_width / image_height

        landscape_mode = False
        page_size = {}


        if ratio > 1.0 :
            landscape_mode = True
            newPdfPage.setPageSize(landscape(A4))
            page_size['width'], page_size['height'] = landscape(A4)
        else:
            newPdfPage.setPageSize(A4)
            page_size['width'], page_size['height'] = A4

        offset_y = 2.0
        offset_x = -1.0
        image_offset_x = 0
        image_offset_y = 0

        print("page size: {0}, {1}".format(page_size['width'], page_size['height']))
        with tempfile.NamedTemporaryFile(mode='w+b',suffix='.jpg') as fp:

            image.save(fp.name,format='jpeg', quality=config.jpeg_quality)

            if config.image_embeded :
                newPdfPage.drawImage(fp.name, 0+image_offset_x, 0+image_offset_y, width=page_size['width'], 
                height=page_size['height'], preserveAspectRatio=True, anchor='s')

        newPdfPage.setFont(config.default_fontname, 10)

        # 文字色と透明度の設定
        newPdfPage.setFillColor(red, alpha=0.0)

        page = ta_pages[i]

        scale = 1.0
        if landscape_mode :
            scale = min(page_size['height'] / image_height, page_size['width'] / image_width)

        else:
            scale = min(page_size['height'] / image_height, page_size['width'] / image_width)

                                
        if is_normalized :
            scale = 1.0
            for block in page.blocks :
                for p in block.paragraphs :
                    for word in p.words :


                        text = ''.join([t.text for t in word.symbols])
                        anchor_y = int(page_size['height'] * ( 1.0 - float(word.bounding_box.normalized_vertices[3].y) )) + offset_y

                        anchor_x = int(page_size['width'] *  float(word.bounding_box.normalized_vertices[3].x)) + offset_x

                        text_height = int( page_size['height']  * (word.bounding_box.normalized_vertices[3].y - word.bounding_box.normalized_vertices[0].y))

                        font_size = text_height

                        newPdfPage.setFont(config.default_fontname, font_size)

                        newPdfPage.drawString(anchor_x, anchor_y, text)

            newPdfPage.showPage()
        else:    

            for block in page.blocks :
                for p in block.paragraphs :
                    for w in p.words :


                        for node in w.symbols :
                            #print(node)
                            
                            anchor_y = image_height  -  int(node.bounding_box.vertices[3].y)
                            anchor_x = int(node.bounding_box.vertices[3].x)

                            text_height = int(node.bounding_box.vertices[3].y) - int(node.bounding_box.vertices[0].y)


                            font_size = config.font_adjustment *  math.floor( text_height / (config.image_resolution / 72 ) )

                            newPdfPage.setFont(config.default_fontname, font_size)

                            newPdfPage.drawString(scale * anchor_x, scale * anchor_y, node.text)

            newPdfPage.showPage()

    newPdfPage.save()

if __name__ == "__main__" :

    # パーサーオブジェクトの初期化
    parser = argparse.ArgumentParser()

    parser.add_argument("imagefile", type=str, help="PDF/TIFF filename(local)")
    parser.add_argument('-s', '--source', type=str, help="Cloud Storage's bukcet gcs-uri for JSON file")
    parser.add_argument('-o', '--output', nargs='?',type=str, help="output PDF filename")

    args = parser.parse_args()

    all_response = get_data_from_gcs(args.source)

    source_image_file = args.imagefile

    # 作成するPDFファイル名
    output_pdf = args.output

    page_list = []

    for response in all_response:
        for page in response.full_text_annotation.pages :
            page_list.append(page)

    if not len(page_list) > 0 :
        sys.exit(-1)

    config = PdfConfig()
#    config.image_embeded = False

    create_pdf(source_image_file, page_list, config, output_pdf)
    