# -*- coding:utf-8 -*-
from adsapi import DailyReport
from config import Config
import pymysql


class PersistentDailyReport:
    def __init__(self, access_token=None):
        if access_token is None:
            raise Exception("Parameter 'access_token' is required.")
        self.access_token = access_token
        self.conf = QADatebase()

    def persist(self, report_date):
        daily_report = DailyReport(report_date=report_date, access_token=self.access_token)
        result = daily_report.__getReport__()
        if result is None:
            return
        db = pymysql.connect(self.conf.HOST, self.conf.USER, self.conf.PWD, self.conf.DB, charset='utf8')
        sql = "INSERT INTO `fb_online_report` (`report_date`, `adaccount_name` \
            , `adaccount_id`, `advertiser`, `campaign_name`, `adset_name`, `ad_name` \
            , `cost`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %f);"
        cursor = db.cursor()
        for record in result:
            sql = sql % (record['insight_date'], record['account_name'], record['account_id']
                         , record['advertiser_id'], record['campaign_group_name']
                         , record['campaign_name'], record['adgroup_name']
                         , record['spend'])
            try:
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                print(e)
        db.close()


class QADatebase:
    def __init__(self):
        conf = Config()
        self.HOST = conf.get('db.qa.url')
        self.USER = conf.get('db.qa.username')
        self.PWD = conf.get('db.qa.password')
        self.DB = conf.get('db.qa.db')

    def __getattr__(self, name):
        self.get(name, None)


if __name__ == "__main__":
    PersistentDailyReport('test').persist('20171116')