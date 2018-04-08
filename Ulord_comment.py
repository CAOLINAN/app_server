# coding=utf-8
# @File  : Ulord_comment.py
# @Author: PuJi
# @Date  : 2018/4/3 0003
from fileHelper import util
from fileHelper.ipfs_module import ulord_transmitter


class Ulord_comment(object):

    def __init__(self, username, filename):
        self.username = username
        self.filename = filename
        self.content_type = util.getType(self.filename)
        self.metadata = MetaData()
        self.password = self.get_password()

    def upload(self):
        self.source_hash = ulord_transmitter.upload(self.filename)

    def set_price(self, amount):
        self.amount = amount

    def set_description(self, description):
        self.metadata.description = description

    def get_password(self):
        password = '123'# TODO query password from the DB
        return password


class MetaData(object):
    def __init__(self):
        self.description = ''  # 描述
        self.language = 'en'  # 平台层?
        self.title = "test"
        self.author = "test"  #
        self.nsfw = False  # 平台层
        self.licenseUrl = '' # ?
        self.preview = ''  # 预览 二进制或者预览内容存入IPFS的hash值
        self.thumbnail = ''  # ?
        self.tag = []  # string list 标签

    def set_default(self, nsfw, licenseUrl, thumbnail):
        self.nsfw = nsfw
        self.licenseUrl = licenseUrl
        self.thumbnail = thumbnail

    def set_comment(self, title, author, tag, preview='', language='en', description=''):
        self.description = description  # 描述
        self.language = language  # 平台层?
        self.title = title
        self.author = author
        self.preview = preview  # 预览 二进制或者预览内容存入IPFS的hash值
        self.tag = tag  # string list 标签
