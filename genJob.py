from storeDB import PersistentDailyReport
from genCSV import CsvGenerate
from genFigure import gen_all
from datetime import datetime, timedelta


REPORT_DATE_FORMAT = '%Y%m%d'


class FmpConsumeReportJob:
    def __init__(self, from_date=None, report_date=None, gen_figure=True):
        self._from_date = from_date
        self._report_date = report_date
        self._gen_figure = gen_figure

    def __dojob__(self, report_date):
        # store records to qa db
        PersistentDailyReport().persist(report_date)
        # generate csv file
        CsvGenerate().__genCsv__(report_date=report_date)

    def fire(self):
        task_list = []
        if self._from_date:
            from_date = datetime.strptime(self._from_date, REPORT_DATE_FORMAT)
            to_date = datetime.strptime(self._report_date, REPORT_DATE_FORMAT)
            if from_date >= to_date:
                raise RuntimeError("from_date should ahead of report_date")
            while from_date < to_date:
                temp_str = from_date.strftime(REPORT_DATE_FORMAT)
                task_list.append(temp_str)
                from_date = from_date + timedelta(days=1)
        task_list.append(self._report_date)
        print('Job for:')
        print(task_list)
        for t in task_list:
            self.__dojob__(t)

        if self._gen_figure:
            gen_all()


def daily_job():
    now_time = datetime.now()
    report_time = now_time + timedelta(days=-1)
    report_date = report_time.strptime(REPORT_DATE_FORMAT)
    FmpConsumeReportJob(report_date=report_date).fire()


if __name__ == '__main__':
    FmpConsumeReportJob(report_date='20171212').fire()
