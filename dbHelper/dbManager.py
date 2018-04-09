# coding=utf-8
# @File  : dbManager.py
# @Author: PuJi
# @Date  : 2018/4/4 0004
from dbhelper import check_version, engine
import sqlalchemy

if check_version():
    metadata = sqlalchemy.MetaData(engine)
    # users_table = sqlalchemy.Table('users',
    #                                metadata,
    #                                sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    #                                sqlalchemy.Column('name', sqlalchemy.String(40)),
    #                                sqlalchemy.Column('email', sqlalchemy.String(40)),
    #                                sqlalchemy.Column('phone', sqlalchemy.String(40)),
    #                                sqlalchemy.Column('ulord_password', sqlalchemy.String(40)),
    #                                sqlalchemy.Column('password', sqlalchemy.String(40))
    #                                )
    # users_table.create()

    files_table = sqlalchemy.Table('files',
                                      metadata,
                                      sqlalchemy.Column('id',sqlalchemy.Integer, primary_key=True),
                                      sqlalchemy.Column('filehash', sqlalchemy.String(46)),
                                      sqlalchemy.Column('name',sqlalchemy.String(40)),
                                      # sqlalchemy.Column('local_path', sqlalchemy.String(46))
                                   # TODO foreign key userid
                                   )
    files_table.create()

    # downloads_table = sqlalchemy.Table('downloads',
    #                                   metadata,
    #                                   sqlalchemy.Column('id',sqlalchemy.Integer, primary_key=True),
    #                                   sqlalchemy.Column('filehash', sqlalchemy.String(46)),
    #                                   sqlalchemy.Column('chunks',sqlalchemy.String()),
    #                                   sqlalchemy.Column()
    #                                   # sqlalchemy.Column('user_id'),sqlalchemy.Integer)# TODO foreign key userid
    #                                    )
    # downloads_table.create()