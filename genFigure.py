from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
from dbconnection import DBConnection
from defaultStorePath import determine_default_file_path


mpl.rcParams['font.sans-serif'] = ['SimHei']
baseline_value = 1000


def gen_last_7_day_chart():
    print('gen_last_7_day_chart start')
    results1 = get_records(last_7_days_sql())
    x_date = []
    y_cost = []
    for row in results1:
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
    plt.close()
    print('gen_last_7_day_chart done')


def gen_12_week_chart():
    print('gen_12_week_chart start')
    results2 = get_records(last_12_week_sql())
    x_date = []
    y_cost = []
    for row in results2:
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
    plt.text(5, baseline_value, 'Baseline 1000', size=15)
    plt.grid(True)
    plt.axhline(baseline_value, linewidth=2)
    file_name = determine_default_file_path('Figure_2', 'png')
    plt.savefig(file_name)
    plt.close()
    print('gen_12_week_chart done')


def gen_total_consume_chart():
    print('gen_total_consume_chart start')
    result3 = get_record(total_consume_sql())
    data = [result3[0], result3[1]]
    title = ['FMP要求消耗', 'Performad统计消耗（' + result3[2] + '）']
    plt.title('Performad总消耗统计')
    plt.bar(title, data, fc='r', width=0.4)
    plt.text(0, result3[0] + 3000, result3[0])
    plt.text(1, result3[1] + 3000, result3[1])
    file_name = determine_default_file_path('Figure_3', 'png')
    plt.savefig(file_name)
    plt.close()
    print('gen_total_consume_chart done')


def gen_60_day_advertiser_consume():
    print('gen_60_day_advertiser_consume start')
    param = advertiser_60_day_consume_param()
    results4 = get_records(param['sql'])
    x_label = []
    data = []
    for row in results4:
        x_label.append(row[0])
        data.append(row[1])
    length = len(x_label)
    index = 0
    while index < length:
        plt.text(x_label[index], data[index], data[index])
        index = index + 1
    plt.axhline(baseline_value, color='b')
    plt.title("Performad消耗-by广告主（" + param['from'] + "-" + param['to'] + "）")
    plt.bar(x_label, data, fc='r', width=0.4)
    file_name = determine_default_file_path('Figure_4', 'png')
    plt.savefig(file_name)
    plt.close()
    print('gen_60_day_advertiser_consume done')


def gen_12_week_bar():
    print('gen_12_week_bar start')
    result5 = get_record(total_12_week_consume_sql())
    plt.title("Performad统计近12周消耗（" + result5[1] + "）")
    plt.bar('FMP要求消耗', 100000, fc='r', width=0.4)
    plt.bar('Performad统计消耗（近12周）', result5[0], fc='r', width=0.4)
    plt.text(0, 100000, 100000)
    plt.text(1, result5[0], result5[0])
    file_name = determine_default_file_path('Figure_5', 'png')
    plt.savefig(file_name)
    plt.close()
    print('gen_12_week_bar done')


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


def get_record(sql):
    conn = DBConnection().get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
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


def total_consume_sql():
    return """select count(weeks) * 1000 baseline
        , sum(cost) cost
        , CONCAT(min(from_date), '-', max(to_date)) time_range
        from (
        select DATE_FORMAT(str_to_date(report_date, '%Y/%m/%d'), '%Y%u') weeks
        , min(DATE_FORMAT(str_to_date(report_date, '%Y/%m/%d'), '%Y.%m.%d')) from_date
        , max(DATE_FORMAT(str_to_date(report_date, '%Y/%m/%d'), '%Y.%m.%d')) to_date
        , round(sum(cost), 2) cost
        from fb_online_report
        group by weeks
        ) a"""


def advertiser_60_day_consume_param():
    d = datetime.datetime.now()
    d1 = d + timedelta(days=-1)
    d2 = d1 + timedelta(days=-60)
    a = d1.strftime("%Y/%m/%d")
    b = d2.strftime("%Y/%m/%d")
    sql =  """select advertiser, round(sum(cost), 2) cost from fb_online_report
         where str_to_date(report_date, '%Y/%m/%d') BETWEEN '""" \
         + b + "' and '" + a +"' group by advertiser order by cost desc"
    result = {'sql': sql, 'from': b, 'to': a}
    return result


def total_12_week_consume_sql():
    return """select sum(cost) cost
    , CONCAT(min(from_date), '-', max(to_date)) time_range
    from (
    select DATE_FORMAT(str_to_date(report_date, '%Y/%m/%d'), '%Y%u') weeks
    , min(DATE_FORMAT(str_to_date(report_date, '%Y/%m/%d'), '%Y.%m.%d')) from_date
    , max(DATE_FORMAT(str_to_date(report_date, '%Y/%m/%d'), '%Y.%m.%d')) to_date
    , round(sum(cost), 2) cost
    from fb_online_report
    group by weeks order by weeks desc limit 12
    ) a"""


def gen_all():
    gen_last_7_day_chart()
    gen_12_week_chart()
    gen_total_consume_chart()
    gen_60_day_advertiser_consume()
    gen_12_week_bar()


if __name__ == '__main__':
    gen_all()