# coding=utf-8
# @File  : Using_API.py
# @Author: PuJi
# @Date  : 2018/4/3 0003
import sys

from fileHelper.ipfs_module import ulord_transmitter
from dbHelper import dbhelper
from fileHelper import util
import json
import requests

# metadata = {"license": "ULORD Inc", "description": "",  # 1
#                 "language": "en",  # 1
#                 "title": "What is LBRY?",  # 1
#                 "author": "Samuel Bryan",  # 1
#                 "nsfw": False,  # 1
#                 "licenseUrl": "",  # 1
#                 "preview": "", "thumbnail": "https://s3.amazonaws.com/files.lbry.io/logo.png",  # 1
#                 "tag": ["action"]}
#
# source = {
#     "source": "d5169241150022f996fa7cd6a9a1c421937276a3275eb912790bd07ba7aec1fac5fd45431d226b8fb402691e79aeb24b",
#     "contentType": "video/mp4"}
#
# fee = {"currency": "ULD", "address": "uW9sdd8AtnNAzMdTD6r9bKmvURSzd2rgXU",  # 2
#        "amount": 1.2}
#
# username = 'justin'
#
# sourcename = 'go-ipfs_v0.4.14_linux-amd64.tar.gz'


source_metadata = {
    'metadata': {
        "license": "LBRY Inc",
        "description": "What is LBRY? An introduction with Alex Tabarrok",
        "language": "en",
        "title": "What is LBRY?",
        "author": "Samuel Bryan",
        "nsfw": False,
        "licenseUrl": "",
        "preview": "",
        "thumbnail": "https://s3.amazonaws.com/files.lbry.io/logo.png",
        "tag": ["action"]
    },
        'source_hash' : "d5169241150022f996fa7cd6a9a1c421937276a3275eb912790bd07ba7aec1fac5fd45431d226b8fb402691e79aeb24b",
        'content_type' : "video/mp4",
        'currency' : "ULD",
        'amount' : 1.2,

        'username' : 'default_wallet',
        'sourcename' : r'E:\ipfs\go-ipfs\ipfs.exe',
        'password':'123'
}


def publish(upload_file):
    url = 'http://192.168.14.67:5000/v1/transactions/publish/'
    source_metadata['sourcename'] = upload_file
    source_metadata['metadata']['author'] = source_metadata.get('username')
    source_metadata['content_type'] = util.getType(source_metadata.get('sourcename'))
    source_metadata['source_hash'] = str(ulord_transmitter.upload(source_metadata.get('sourcename')))
    # save file info in DB
    new_file = dbhelper.File(name=util.getName(source_metadata.get('sourcename')), hash=source_metadata['source_hash'])
    source_metadata['sourcename'] = util.getPureName(source_metadata.get('sourcename'))

    try:
        dbhelper.session.add(new_file)
        dbhelper.session.commit()
        dbhelper.session.close()
    except:
        print("Error save data in DB.Rollback.")
        dbhelper.session.rollback()

    if source_metadata['source_hash']:
        import pprint
        pprint.pprint(source_metadata)
        print("hash:{}".format(source_metadata.get('source_hash')))
        res = requests.post(url, json=source_metadata, headers={'appkey': "03e410a136ec11e8adaff48e3889c8ab"})
        # print(res)
        # print(res.json())
        print (res.json().get('reason'))


# user register
def register():
    url = 'http://192.168.14.67:5000/v1/users/reg/'
    meta_data = {
        'username' : 'username',
        'password' : 'password',
        'email' : 'email',
        'appname' : 'appname',
        'appdes' : 'appdes'
    }
    json_string = json.dumps(meta_data)
    print(json_string)
    appkey = requests.post(url, json=json.loads(json_string))
    print (appkey.json())


def login(username, password):
    url = 'http://192.168.14.67:5000/v1/users/login/'
    meta_data = {
        'username': username,
        'password': password
    }
    json_string = json.dumps(meta_data)
    appkey = requests.post(url, json=json.loads(json_string))
    print (appkey.json().get())


def download(hash):
    ulord_transmitter.downloadhash(hash)
    try:
        print(hash)
        print(type(hash))
        current_file = dbhelper.session.query(dbhelper.File).filter(dbhelper.File.hash == hash).one()
        # dbhelper.session.commit()
        # dbhelper.session.close()
        # print (current_file.name)
        util.changeName(hash, current_file.name)
    except:
        print("Error query data in DB.Rollback.")
        dbhelper.session.rollback()


if __name__ == '__main__':
    # login()
    print(sys.argv)
    arg = sys.argv[1]
    if arg == 'register':
        register()
    elif arg == 'login':
        login(sys.argv[2], sys.argv[3])
    elif arg == 'publish':
        if len(sys.argv) == 3:
            publish(sys.argv[2])
        else:
            publish(r'E:\ipfs\go-ipfs\ipfs.exe')
    elif arg == 'download':
        download(sys.argv[2])

