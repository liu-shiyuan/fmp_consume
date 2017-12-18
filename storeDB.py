# -*- coding:utf-8 -*-
from adsapi import DailyReport
from dbconnection import DBConnection


class PersistentDailyReport:
    def __init__(self):
        """"""

    def persist(self, report_date):
        daily_report = DailyReport(report_date=report_date)
        result = daily_report.__getReport__()
        if result is None:
            print('No consume at %s' % report_date)
            return
        self.removeOldRecords(report_date)
        conn = DBConnection().get_connection()
        sql = "INSERT INTO `fb_online_report` (`report_date`, `adaccount_name` \
            , `adaccount_id`, `advertiser`, `campaign_name`, `adset_name`, `ad_name` \
            , `cost`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %f);"
        cursor = conn.cursor()
        for record in result:
            final_sql = sql % (self.getDbDateFormat(record['insight_date']), record['account_name'], record['account_id']
                         , record['advertiser_id'], record['campaign_group_name']
                         , record['campaign_name'], record['adgroup_name']
                         , record['spend'])
            try:
                cursor.execute(final_sql)
                conn.commit()
            except Exception as e:
                print(e)
        conn.close()

    def removeOldRecords(self, report_date):
        conn = DBConnection().get_connection()
        sql = "delete from fb_online_report where report_date = '%s';"
        param_date = self.getDbDateFormat(report_date)
        final_sql = sql % param_date
        conn = DBConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute(final_sql)
        conn.commit()
        conn.close()

    def getDbDateFormat(self, report_date):
        """ YYYYMMDD -> YYYY/MM/DD, YYYY-MM-DD -> YYYY/MM/DD"""
        report_date = report_date.replace('-', '')
        year_str = report_date[0:4]
        month_str = report_date[5] if report_date[4] == '0' else report_date[4:6]
        day_str = report_date[7] if report_date[6] == '0' else report_date[6:8]
        param_date = year_str + '/' + month_str + '/' + day_str
        return param_date


if __name__ == "__main__":
    PersistentDailyReport().persist('20171213')