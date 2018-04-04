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
    #                                sqlalchemy.Column('password', sqlalchemy.String(120))
    #                                )
    # users_table = sqlalchemy.Table('users', metadata, autoload=True)
    # users_table.create()

    files_table = sqlalchemy.Table('files',
                                      metadata,
                                      # sqlalchemy.Column('id',sqlalchemy.Integer, primary_key=True),
                                      sqlalchemy.Column('hash', sqlalchemy.String(46), primary_key=True),
                                      sqlalchemy.Column('name',sqlalchemy.String(40))
                                      # sqlalchemy.Column('hash', sqlalchemy.String(46))
                                      )
    files_table.create()

    # comments_table = sqlalchemy.Table('comments',
    #                                   metadata,
    #                                   sqlalchemy.Column('id',sqlalchemy.Integer, primary_key=True),
    #                                   sqlalchemy.Column('')
    #                                   )
    #
    # comments_table.create()