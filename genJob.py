from storeDB import PersistentDailyReport
from genCSV import CsvGenerate
from genFigure import gen_all
#import datetime.datetime
#import datetime.timedelta
from datetime import datetime, timedelta


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
            from_date = datetime.strptime(self._from_date, '%Y%m%d')
            to_date = datetime.strptime(self._report_date, '%Y%m%d')
            if from_date >= to_date:
                raise RuntimeError("from_date should ahead of report_date")
            while from_date < to_date:
                temp_str = from_date.strftime("%Y%m%d")
                task_list.append(temp_str)
                from_date = from_date + timedelta(days=1)
        task_list.append(self._report_date)
        print('Job for:')
        print(task_list)
        for t in task_list:
            self.__dojob__(t)

        if self._gen_figure:
            gen_all()


if __name__ == '__main__':
    FmpConsumeReportJob(from_date='20171214', report_date='20171217').fire()
    #FmpConsumeReportJob(report_date='20171212').fire()