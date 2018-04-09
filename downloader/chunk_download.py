# coding=utf-8
# @File  : chunk_download.py
# @Author: PuJi
# @Date  : 2018/4/8 0008

# TianheCloud
import json
import os

from fileHelper.ipfs_module import UlordTransmitter
from fileHelper import util

ipfs_host = '114.67.37.2'
ipfs_port = '20418'


def chunkdownload(hash, filepath=None):
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
                        'success': ulord_transmitter.downloadhash(link.get('Hash'),filepath)
                    }
                })
            i += 1
        print(ulord_transmitter.chunks)
        # TODO save ulord_transmitter.chunks in the DB
    else:
        print("no chunks")

def saveChunksResult(filehash):
    # save the chunks result into the "download/filehash/temp.json"
    ulord_transmitter = UlordTransmitter(ipfs_host, ipfs_port)
    # ulord_transmitter.upload()
    ulord_transmitter.list(filehash)
    if ulord_transmitter.links:
        i = 0
        for link in ulord_transmitter.links:
            if 'Hash' in link.keys():
                ulord_transmitter.chunks.update({
                    i: {
                        'filehash': link.get('Hash'),
                        'success': False
                    }
                })
            i += 1
        download_path = os.path.join(util.getRootPath(), 'download')
        util.saveFile(os.path.join(os.path.join(download_path, filehash), 'temp.json'), json.dumps(ulord_transmitter.chunks))
    else:
        print("no chunks")


def resumabledownload(filehash):
    download_path = os.path.join(util.getRootPath(), 'download')
    filehash_path = os.path.join(download_path, filehash)
    tempjson = os.path.join(filehash_path, 'temp.json')
    with open(tempjson) as target_file:
        print target_file
        chunks = json.load(target_file)
    if chunks:
        for chunk, chunk_result in chunks.iteritems():
            if not chunk_result.get('success'):
                ulord_transmitter = UlordTransmitter(ipfs_host, ipfs_port)
                chunk_result['success'] = ulord_transmitter.downloadhash(chunk_result.get('filehash'), filehash_path) or chunk_result.get('success')
                util.saveFile(tempjson, json.dumps(chunks))


def resumableMerge(filehash):
    download_path = os.path.join(util.getRootPath(), 'download')
    filehash_path = os.path.join(download_path, filehash)
    tempjson = os.path.join(filehash_path, 'temp.json')
    with open(tempjson) as jsonfile:
        # print jsonfile
        chunks = json.load(jsonfile)
    if chunks:
        localfile = os.path.join(filehash_path, filehash)
        with open(localfile, 'wb') as target_file:
            for i in range(len(chunks)):
                # print(chunks)
                # print(type(chunks))
                # print(chunks.get(str(i)))
                chunk = os.path.join(filehash_path, chunks.get(str(i)).get('filehash'))
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


def mutilprocessdownload(filehash):
    # start mutil processes to download

    saveChunksResult(filehash)

    # TODO mutilprocess download


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
    # merge(test_hash)
    # saveChunksResult(test_hash)
    # resumabledownload(test_hash)
    # resumableMerge(test_hash)
    ulord_test_resumable_download = UlordTransmitter(ipfs_host, ipfs_port)
    ulord_test_resumable_download.resumableMerge(test_hash, "go-ipfs_v0.4.14_linux-amd64.tar.gz")