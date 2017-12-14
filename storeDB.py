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
            return
        conn = DBConnection().get_connection()
        sql = "INSERT INTO `fb_online_report` (`report_date`, `adaccount_name` \
            , `adaccount_id`, `advertiser`, `campaign_name`, `adset_name`, `ad_name` \
            , `cost`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %f);"
        cursor = conn.cursor()
        for record in result:
            final_sql = sql % (record['insight_date'], record['account_name'], record['account_id']
                         , record['advertiser_id'], record['campaign_group_name']
                         , record['campaign_name'], record['adgroup_name']
                         , record['spend'])
            try:
                cursor.execute(final_sql)
                conn.commit()
            except Exception as e:
                print(e)
        conn.close()


if __name__ == "__main__":
    PersistentDailyReport().persist('20171116')