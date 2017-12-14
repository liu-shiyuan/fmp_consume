from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
from dbconnection import DBConnection
from defaultStorePath import determine_default_file_path


mpl.rcParams['font.sans-serif'] = ['SimHei']


def gen_last_7_day_chart():
    results = get_records(last_7_days_sql())
    x_date = []
    y_cost = []
    for row in results:
        x_date.append(row[1])
        y_cost.append(row[2])

    plt.plot(x_date, y_cost, 'ro-')
    plt.title('Performad近七日消耗统计')
    length = len(x_date)
    index = 0
    while index < length:
        plt.text(x_date[index], y_cost[index], y_cost[index])
        index = index + 1
    plt.grid(True)
    file_name = determine_default_file_path('Figure_1', 'png')
    plt.savefig(file_name)


def gen_12_week_chart():
    results = get_records(last_12_week_sql())
    x_date = []
    y_cost = []
    for row in results:
        x_date.append(row[1] + '-' + row[2])
        y_cost.append(row[3])
    fig1 = plt.figure(figsize=(20, 10))
    plt.xticks(rotation=60)
    plt.plot(x_date, y_cost, 'ro-')
    plt.title('Performad每周消耗统计')
    length = len(x_date)
    index = 0
    while index < length:
        plt.text(x_date[index], y_cost[index], y_cost[index], rotation=75)
        index = index + 1
    plt.text(5, 1000, 'Baseline 1000', size=15)
    plt.grid(True)
    plt.axhline(1000, linewidth=2)
    file_name = determine_default_file_path('Figure_2', 'png')
    plt.savefig(file_name)


def get_records(sql):
    conn = DBConnection().get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(e)
    conn.close()


def last_7_days_sql():
    d = datetime.datetime.now()
    d1 = d + timedelta(days=-1)
    d2 = d1 + timedelta(days=-7)

    a = d1.strftime("%Y/%m/%d")
    b = d2.strftime("%Y/%m/%d")
    sql = """select str_to_date(report_date, '%Y/%m/%d') rank,
    DATE_FORMAT(str_to_date(report_date, '%Y/%m/%d'), '%m月%d日') date , round(sum(cost), 2) cost
    from fb_online_report
    where str_to_date(report_date, '%Y/%m/%d') BETWEEN '""" \
    + b + "' and '" + a + "' group by report_date order by rank"
    return sql


def last_12_week_sql():
    return """select DATE_FORMAT(str_to_date(report_date, '%Y/%m/%d'), '%Y%u') weeks
    , min(DATE_FORMAT(str_to_date(report_date, '%Y/%m/%d'), '%m.%d')) from_date
    , max(DATE_FORMAT(str_to_date(report_date, '%Y/%m/%d'), '%m.%d')) to_date
    , round(sum(cost), 2) cost
    from fb_online_report
    group by weeks
    order by weeks """


if __name__ == '__main__':
    #gen_last_7_day_chart()
    gen_12_week_chart()