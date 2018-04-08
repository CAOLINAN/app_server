# coding=utf-8
# @File  : chunk_download.py
# @Author: PuJi
# @Date  : 2018/4/8 0008

# TianheCloud
ipfs_host = '114.67.37.2'
ipfs_port = '20418'
import os

from fileHelper.ipfs_module import UlordTransmitter


def chunkdownload(hash):
    ulord_transmitter = UlordTransmitter(ipfs_host, ipfs_port)
    # ulord_transmitter.upload()
    ulord_transmitter.list(hash)
    if ulord_transmitter.links:
        # print(ulord_transmitter.links)
        i = 0
        # print(len(ulord_transmitter.links))
        for link in ulord_transmitter.links:
            if 'Hash' in link.keys():
                ulord_transmitter.chunks.update({
                    link.get('Hash'):{
                        'chunk': i,
                        'success': ulord_transmitter.downloadhash(link.get('Hash'))
                    }
                })
            i += 1
        print(ulord_transmitter.chunks)
        # TODO save ulord_transmitter.chunks in the DB
    else:
        print("no chunks")


def savefile(localfile, chunks):
    with open(localfile, 'wb') as target_file:
        for chunk in chunks:
            with open(chunk, 'rb') as source_file:
                for line in source_file:
                    target_file.write(line)
            try:
                os.remove(chunk)  # 删除该分片，节约空间
            except Exception, e:
                print("{0}:{1} remove failed:{2}".format(chunk, os.path.isfile(chunk), e))


def merge(hash):
    ulord_transmitter = UlordTransmitter(ipfs_host, ipfs_port)
    # ulord_transmitter.upload()
    ulord_transmitter.list(hash)
    if ulord_transmitter.links:
        chunk_list = []
        for link in ulord_transmitter.links:
            if 'Hash' in link.keys():
                chunk_list.append(link.get('Hash'))
        savefile('go-ipfs_v0.4.14_linux-amd64.tar.gz', chunk_list)
    else:
        print("no chunks")


if __name__ == '__main__':

    test_hash = "QmT4kFS5gxzQZJwiDJQ66JLVGPpyTCF912bywYkpgyaPsD"
    # chunkdownload(test_hash)
    merge(test_hash)