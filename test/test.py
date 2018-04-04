# coding=utf-8
# @File  : test.py
# @Author: PuJi
# @Date  : 2018/4/3 0003

import requests

source_metadata = {
    'metadata': {
        "license": "LBRY Inc",
        "description": "What is LBRY? An introduction with Alex Tabarrok",
        "language": "en",
        "title": "What is LBRY?",
        "author": "Samuel Bryan",
        "version": "_0_1_0",
        "nsfw": False,
        "licenseUrl": "",
        "preview": "",
        "thumbnail": "https://s3.amazonaws.com/files.lbry.io/logo.png",
        "tag": ["action"]
    },
    'source':{
        "source": "d5169241150022f996fa7cd6a9a1c421937276a3275eb912790bd07ba7aec1fac5fd45431d226b8fb402691e79aeb24b",
        "version": "_0_0_1",
        "contentType": "video/mp4",
        "sourceType": "unet_sd_hash"
    },

    'fee': {
        "currency": "ULD",
        "address": "uW9sdd8AtnNAzMdTD6r9bKmvURSzd2rgXU",
        "amount": 1.2
    },

    'username':'justin',
    'sourcename': r'E:\ipfs\go-ipfs\ipfs.exe'
}

url = 'http://192.168.14.40:5000/test'

res = requests.post(url, json=source_metadata)