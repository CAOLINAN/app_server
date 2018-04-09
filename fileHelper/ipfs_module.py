# coding=utf-8
# @File  : ipfs_module.py
# @Author: PuJi
# @Date  : 2018/4/3 0003

import time, ipfsapi
import logging
# import requests
import os
import json
import util


class UlordTransmitter():
    # download and upload files from Ulord
    def __init__(self, host='127.0.0.1', port='5001'):
        self.ipfs_host = host
        self.ipfs_port = port
        self.connect = ipfsapi.connect(self.ipfs_host, self.ipfs_port)
        self.log = ""
        self.chunks = {}
        self.objects = None
        self.links = []
        self.downloadpath = os.path.join(util.getRootPath(), 'download')

    def update(self, host='127.0.0.1', port='5001'):
        self.ipfs_host = host
        self.ipfs_port = port
        self.connect = ipfsapi.connect(self.ipfs_host, self.ipfs_port)
        self.log = ""
        self.chunks = {}
        self.objects = None
        self.links = []

    def upload(self, local_file):
        try:
            start = time.time()
            result = self.connect.add(local_file)
            end = time.time()
            print('upload {0} ,size is {1}, cost:{2}'.format(local_file, util.getSize(local_file), (end - start)))
            # TODO save filename in DB
            return result.get('Hash')
        except Exception, e:
            # TODO save e in the log
            return None

    def list(self, filehash):
        try:
            self.objects = self.connect.ls(filehash).get('Objects')
            if self.objects:
                for object in self.objects:
                    if 'Links' in object.keys():
                        for link in object.get('Links'):
                            self.links.append(link)
            else:
                self.links = "test"
        except Exception, e:
            logging.error("ls fail:{}".format(e))

    def downloadfile(self, localfile):
        # TODO query the file hash from DB
        pass

    def downloadhash(self, filehash, filepath=None):
        try:
            start = time.time()
            self.connect.get(filehash, filepath=filepath)
            end = time.time()
            print('download {0} cost:{1}'.format(filehash, (end - start)))
            print("download {} successfully!".format(filehash))
            return True
        except Exception, e:
            logging.error("download fail:{}".format(e))
            return False

    def resumableMerge(self, filehash, filename=None):
        # not thread safely.single thread
        filehash_path = os.path.join(self.downloadpath, filehash)
        tempjson = os.path.join(filehash_path, 'temp.json')
        if not os.path.isfile(tempjson):
            # save chunks result into the temp.json
            self.list(filehash)
            if self.links:
                i = 0
                for link in self.links:
                    if 'Hash' in link.keys():
                        self.chunks.update({
                            i: {
                                'filehash': link.get('Hash'),
                                'success': False
                            }
                        })
                    i += 1
                util.saveFile(tempjson, json.dumps(self.chunks))
            else:
                print("no chunks.Error get the {} chunks result".format(filehash))
        # download chunk
        with open(tempjson) as target_file:
            self.chunks = json.load(target_file)
        if self.chunks:
            for chunk, chunk_result in self.chunks.iteritems():
                if not chunk_result.get('success'):
                    chunk_result['success'] = self.downloadhash(chunk_result.get('filehash'), filehash_path) or chunk_result.get('success')
                    util.saveFile(tempjson, json.dumps(self.chunks))
            # merge chunks
            if filename:
                localfile = os.path.join(filehash_path, filename)
            else:
                localfile = os.path.join(filehash_path, filehash)
            with open(localfile, 'wb') as target_file:
                for i in range(len(self.chunks)):
                    chunk = os.path.join(filehash_path, self.chunks.get(str(i)).get('filehash'))
                    with open(chunk, 'rb') as source_file:
                        for line in source_file:
                            target_file.write(line)
                    try:
                        os.remove(chunk)  # 删除该分片，节约空间
                    except Exception, e:
                        print("{0}:{1} remove failed:{2}".format(chunk, os.path.isfile(chunk), e))
                try:
                    os.remove(tempjson)
                except Exception, e:
                    print("{0}:{1} remove failed:{2}".format(tempjson, os.path.isfile(tempjson), e))


# ulord_transmitter = UlordTransmitter()


if __name__ == '__main__':
    # localhost
    ipfs_host = '127.0.0.1'
    ipfs_port = '5001'

    # TianheCloud
    # ipfs_host = '114.67.37.2'
    # ipfs_port = '20418'

    # virtualhost
    # ipfs_host = '192.168.14.45'
    # ipfs_port = '5001'

    local_file = 'go-ipfs_v0.4.14_linux-amd64.tar.gz'
    ulord_transmitter = UlordTransmitter(ipfs_host, ipfs_port)

    # upload
    ulord_transmitter.upload(local_file)

    # download
    # ulord_transmitter.downloadfile(local_file)

    # download
    ulord_transmitter.downloadhash('QmT4kFS5gxzQZJwiDJQ66JLVGPpyTCF912bywYkpgyaPsD')


