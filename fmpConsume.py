import time
import pytz
from datetime import datetime, timedelta
from genJob import FmpConsumeReportJob, daily_job
from config import Config


tz = pytz.timezone('Asia/Shanghai')
conf = Config()
schedule_hour = conf.get('schedule.hour')
schedule_minute = conf.get('schedule.minute')

REPORT_DATE_FORMAT = '%Y%m%d'
_report_date = datetime.now(tz) + timedelta(days=-1)
_from_date = _report_date + timedelta(days=-5)
from_date = _from_date.strftime(REPORT_DATE_FORMAT)
report_date = _report_date.strftime(REPORT_DATE_FORMAT)
print('init date from: %s to: %s' % (from_date, report_date))

FmpConsumeReportJob(from_date=from_date, report_date=report_date).fire()

while True:
    current_time = datetime.now(tz)
    if current_time.hour == schedule_hour and current_time.minute == schedule_minute and current_time.second == 0:
        print('daily_job run')
        daily_job()
        print('daily_job end')
    time.sleep(0.5)
