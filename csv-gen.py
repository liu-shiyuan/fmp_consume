# -*- coding:utf-8 -*-
import csv
import os
import platform
from adsapi import DailyReport
import datetime
import time


class CsvGenerate:
    def __init__(self, access_token=None):
        if access_token is None:
            raise Exception("Parameter 'access_token' is required.")
        self.access_token = access_token

    def __genCsv__(self, report_date=None, path=None):
        if report_date is None:
            raise Exception("Parameter 'report_date' is required.")
        if path is None:
            path = self.__determineDefaultFilePath__(report_date)

        daily_report = DailyReport(report_date=report_date, access_token=self.access_token)
        result = daily_report.__getReport__(True)
        with open(path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            fields = ("insight_date", "account_name", "account_id", "advertiser_id", "campaign_group_name"\
                          , "campaign_name", "adgroup_name", "displayName", "fb_created_time", "spend")
            created_time_format = '%Y/%m/%d %H:%M:%S'
            writer.writerow(self.__getFields__())
            for record in result:
                line = []
                temp_field_value = None
                for title in fields:
                    if title == 'fb_created_time':
                        # unix time -> time
                        unix_time_2_time = time.localtime(record[title] / 1000)
                        # time -> string
                        temp_field_value = time.strftime(created_time_format, unix_time_2_time)
                    elif title == 'insight_date':
                        temp_field_value = str(record[title]).replace('-', '/')
                    else:
                        temp_field_value = str(record[title])
                    line.append(temp_field_value)
                writer.writerow(line)

    @staticmethod
    def __determineDefaultFilePath__(report_date):
        if  'windows' == platform.system().lower():
            base_path = os.getenv('USERPROFILE')
            return base_path + '/Desktop/' + report_date + '.csv'
        elif 'linux' == platform.system().lower():
            base_path = os.getenv('HOME')
            return 'base_path' + '/'
        elif 'darwin' == platform.system().lower():
            base_path = os.getenv('HOME')
            return 'base_path' + '/'

    @staticmethod
    def __getFields__():
        return ("日期", "Ad account name", "Ad account ID", "advertiser"\
                    , "campaign name", "adset name", "ad name", "创建者"\
                    , "创建时间", "cost")


if __name__ == '__main__':
    CsvGenerate(access_token='ss').__genCsv__(report_date='20171116')
