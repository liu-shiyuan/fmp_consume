# -*- coding:utf-8 -*-
import json
import urllib.request
import urllib.parse
import urllib.error
import pprint
import sys
from config import Config


class DailyReport:
    def __init__(self, domain=None, api=None, report_date=None, access_token=None):
        if report_date is None:
            raise Exception("Parameter 'report_date' is required.")
        conf = Config()
        self.domain = domain if domain else conf.get('domain')
        self.api = api if api else conf.get('api')
        self.access_token = access_token if access_token else conf.get('token')
        self.report_date = report_date

    def __getReport__(self, print_result=False):
        dest_url = urllib.parse.urljoin(self.domain, self.api)
        dest_url = urllib.parse.urljoin(dest_url, self.report_date)
        print('dest url: ', dest_url)
        headers = {'accessToken': self.access_token}
        req = urllib.request.Request(dest_url, headers=headers)
        code = None
        try:
            response = urllib.request.urlopen(req)
            json_str = response.read().decode('utf-8')
            code = response.code
            if json_str is None:
                print('Empty result')
            else:
                result = json.loads(json_str)
                print('result size: %s' % len(result))
                if print_result:
                    pprint.pprint(result)
                return result
        except urllib.error.HTTPError as e:
            print('Error Occurred: %s, code: %s' % (e.reason, e.code))


if __name__ == '__main__':
    arg_size = len(sys.argv)
    if arg_size < 3:
        raise Exception("Parameter 'report_date' & 'access_token' are required.")
    _report_date = sys.argv[1]
    _access_token = sys.argv[2]
    dr = DailyReport(report_date=_report_date, access_token=_access_token)
    dr.__getReport__(True)

