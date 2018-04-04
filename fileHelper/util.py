# coding=utf-8
# @File  : util.py
# @Author: PuJi
# @Date  : 2018/4/3 0003
import os


def getSize(filename):
    # get file size
    fsize = os.path.getsize(filename)
    return fsize


def getType(filename):
    # get file type
    if '.' in filename:
        return filename.split('.')[-1]
    else:
        return 'NoType'


def getPureName(filename):
    # get file name
    if '.' in filename:
        filename = filename.split('.')[0]
    if '/' in filename:
        return filename.split('/')[-1]
    elif '\\' in filename:
        return filename.split('\\')[-1]
    else:
        return filename


def getName(filename):
    # get file name
    # if '/' in filename:
    #     return filename.split('/')[-1]
    # elif '\\' in filename:
    #     return filename.split('\\')[-1]
    # else:
    #     return filename
    return os.path.split(filename)[-1]


def changeName(originalname, newname):
    # change file name from a hash to filename
    if os.path.isfile(newname):
        print("Error: File {} has exited!".format(newname))
        return False
    if os.path.isfile(originalname):
        file_path, original_short_name = os.path.split(originalname)
        newname = os.path.join(file_path, newname)
        if os.path.isfile(newname):
            print("Error: File {} has exited!".format(newname))
            return False
        os.rename(originalname, newname)
        return True
    else:
        print("Error: File {} doesn't exist!".format(originalname))
        return False


if __name__ == '__main__':
    print (getPureName('E:\ipfs\go-ipfs\ipfs.exe'))
    print(getSize('E:\ipfs\go-ipfs\ipfs.exe'))
    changeName(r'E:\ulord\app_server\sasas', 'testchange')