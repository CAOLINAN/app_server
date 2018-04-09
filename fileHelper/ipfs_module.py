# coding=utf-8
# @File  : ipfs_module.py
# @Author: PuJi
# @Date  : 2018/4/3 0003

import time, ipfsapi
import logging
# import requests
import os

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

    def downloadchunk(self, filehash):
        self.list(filehash)
        if self.links:
            i = 0
            for link in ulord_transmitter.links:
                if 'Hash' in link.keys():
                    self.chunks.update({
                        link.get('Hash'): {
                            'chunk': i,
                            # 'success': self.downloadhash(link.get('Hash'), os.path.join(self.downloadpath, filehash))
                            'success': False
                        }
                    })
                i += 1
            # print(ulord_transmitter.chunks)
            # TODO save ulord_transmitter.chunks in the file or DB
            # util.saveFile(os.path.join(os.path.join(util.getRootPath(), 'download'), '{}_temp'.format(filehash)), self.chunks)
        else:
            print("no chunks")

    def merge(self, filehash):
        self.list(hash)
        if self.links:
            chunk_list = []
            for link in self.links:
                if 'Hash' in link.keys():
                    if os.path.isfile(os.path.join(os.path.join(self.downloadpath, filehash), link.get('Hash'))):
                        chunk_list.append(link.get('Hash'))
                    else:
                        self.downloadhash(link.get('Hash'),os.path.join(self.downloadpath, filehash))
                        chunk_list.append(link.get('Hash'))
            util.mergeFile('go-ipfs_v0.4.14_linux-amd64.tar.gz', chunk_list)
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


