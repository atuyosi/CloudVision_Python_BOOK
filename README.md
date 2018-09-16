
# このリポジトリについて

『Google Cloud Vision APIとPythonで文字認識』の関連ファイルのリポジトリです。

## ディレクトリ構成

### 第3章

- basic : 第3章 前半
- advanced : 第3章 後半

### 第4章

- storage : Google Cloud Storage関連
- async : PDF/TIFFからの文字認識（非同期）

### 第5章

- generate_pdf : ReportLabによるPDF生成

## セットアップ

```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

### 実行に関する注意

Google Cloud Vision APIの認証情報を記載したJSONファイルへのパスを`GOOGLE_APPLICATION_CREDENTIALS`にセットする必要があります。

```
$ export GOOGLE_APPLICATION_CREDENTIALS=/patho/to/your-credentials.json
```


## そのほか

### 画像データについて

`image_data`ディレクトリの画像うち、Webから入手したものは以下のとおりです。

- 日本語版Wikipediaの[「光学文字認識」](https://ja.wikipedia.org/wiki/光学文字認識)のページの一部（`about_ocr.png`）
- [プログラマが知るべき97のこと/DRY原則 - Wikisource](https://ja.wikisource.org/wiki/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9E%E3%81%8C%E7%9F%A5%E3%82%8B%E3%81%B9%E3%81%8D97%E3%81%AE%E3%81%93%E3%81%A8/DRY%E5%8E%9F%E5%89%87)（`dry_image.pdf`）
- 英語版Wikipediaの[OCR](https://en.wikipedia.org/wiki/Optical_character_recognition)のページ（`output_multi.tiff`）

###  pathlibについて

ソースコードからサンプルデータにアクセスするパスの解決のために[`pathlib`](https://docs.python.org/ja/3.7/library/pathlib.html)を使用しています。

追加のモジュールのインストールは不要です。

