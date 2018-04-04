# coding=utf-8
# @File  : ipfs_module.py
# @Author: PuJi
# @Date  : 2018/4/3 0003

import time, ipfsapi
import logging
# import requests
import util


class UlordTransmitter():
    # download and upload files from Ulord
    def __init__(self, host='127.0.0.1', port='5001'):
        self.ipfs_host = host
        self.ipfs_port = port
        self.connect = ipfsapi.connect(self.ipfs_host, self.ipfs_port)
        self.log = ""

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

    def downloadfile(self, localfile):
        # TODO query the file hash from DB
        pass

    def downloadhash(self, hash):
        try:
            start = time.time()
            self.connect.get(hash)
            end = time.time()
            print('download {0} cost:{1}'.format(hash, (end - start)))
            print("download {} successfully!".format(hash))
            return True
        except Exception, e:
            logging.error("download fail:{}".format(e))
            return None

ulord_transmitter = UlordTransmitter()


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


