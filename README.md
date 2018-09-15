
# このリポジトリについて

『Google Cloud Vison APIとPythonで文字認識』の関連ファイルのリポジトリです。

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

###  pathlibについて

ソースコードからサンプルデータにアクセスするパスの解決のために[`pathlib`](https://docs.python.org/ja/3.7/library/pathlib.html)を使用しています。

追加のモジュールのインストールは不要です。

