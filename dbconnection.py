# -*- coding:utf-8 -*-
from config import Config
import pymysql


class QADatebase:
    def __init__(self):
        conf = Config()
        self.HOST = conf.get('db.qa.url')
        self.USER = conf.get('db.qa.username')
        self.PWD = conf.get('db.qa.password')
        self.DB = conf.get('db.qa.db')

    def __getattr__(self, name):
        self.get(name, None)


class DBConnection:
    def __init__(self):
        self.conf = QADatebase()
        self.conn = None

    def get_connection(self, db=None):
        if db:
            self.conn = pymysql.connect(self.conf.HOST, self.conf.USER, self.conf.PWD, db, charset='utf8')
        else:
            self.conn = pymysql.connect(self.conf.HOST, self.conf.USER, self.conf.PWD, self.conf.DB, charset='utf8')
        return self.conn
