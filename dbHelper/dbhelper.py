# coding=utf-8
# @File  : dbhelper.py
# @Author: PuJi
# @Date  : 2018/4/3 0003

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

current_version = '1.2.6'
def check_version():
    if sqlalchemy.__version__ == current_version:
        return True
    else:
        print("sqlalchemy's is not supported!\n exit...")
        exit(-1)

check_version()
dbpath = r'E:\ulord\app_server\dbHelper\app.db'
engine = sqlalchemy.create_engine('sqlite:///{}'.format(dbpath), echo=True) # create an sql engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    email = Column(String(40))
    phone = Column(String(40))
    password = Column(String(40))


class File(Base):
    __tablename__ = 'files'
    # id = Column(Integer, primary_key=True)
    hash = Column(String(46), primary_key=True)
    name = Column(String(40))


session = sessionmaker(bind=engine)()












