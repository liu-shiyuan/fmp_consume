# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from config import Config
from datetime import datetime, timedelta
from defaultStorePath import _get_base_path

conf = Config()

mail_host = conf.get('mail.service')
mail_user = conf.get('mail.user')
mail_pwd = conf.get('mail.pwd')
mail_port = conf.get('mail.port')
mail_admin_raw = conf.get('mail.admin')
mail_admin = []
for e in mail_admin_raw.split(','):
    mail_admin.append(e.strip())
mail_receives_raw = conf.get('mail.receives')
mail_receives = []
for e in mail_receives_raw.split(','):
    mail_receives.append(e.strip())
mail_cc_raw = conf.get('mail.cc')
mail_cc = []
for e in mail_cc_raw.split(','):
    mail_cc.append(e.strip())


def get_mail_client():
    _mail_client = smtplib.SMTP(host=mail_host, port=mail_port)
    _mail_client.login(user=mail_user, password=mail_pwd)
    return _mail_client


def sent_job_status_to_admin(report_date, content=None):
    default_text = 'Daily fmp consume job finish: %s' % report_date
    if content:
        message = MIMEText(content, 'Plain', 'utf-8')
    else:
        message = MIMEText(default_text, 'Plain', 'utf-8')
    subject = 'FMP consume'
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = mail_user
    message['To'] = mail_admin_raw
    mail_client = get_mail_client()
    try:
        mail_client.sendmail(mail_user, mail_admin, message.as_string())
        print('sent_job_status_to_admin succeed')
    except smtplib.SMTPException:
        print("Error: sent_job_status_to_admin无法发送邮件")
    mail_client.quit()


def sent_report_to_receives():
    yesterday_date = datetime.now() + timedelta(days=-1)
    time_range = '2017.3.20-%s' % yesterday_date.strftime('%Y.%m.%d')
    subject = 'FMP累计消耗统计（%s）' % time_range
    msg_root = MIMEMultipart('related')
    msg_root['From'] = mail_user
    msg_root['To'] = mail_receives_raw
    if mail_cc_raw is not None and mail_cc_raw != '':
        msg_root['Cc'] = mail_cc_raw
    msg_root['Subject'] = Header(subject, 'utf-8')
    mail_msg = """
    Hi all：<br>
    Performad生产环境消耗统计从%s的数据<br><br>
    一、Performad近七日消耗统计<br>
    <p><img src="cid:Figure_1"></p>
    二、Performad每周消耗统计<br>
    <p><img src="cid:Figure_2"></p>
    三、Performad总消耗统计<br>
    <p><img src="cid:Figure_3"></p>
    四、Performad分广告主消耗统计<br>
    <p><img src="cid:Figure_4"></p>
    五、Performad近12周消耗统计<br>
    <p><img src="cid:Figure_5"></p>
    注：蓝色线为1000美元基准线<br>
    <br>
    <p>FMP dashboard:  <a href="http://172.16.25.197:8080/fmp/dashboard.html">http://172.16.25.197:8080/fmp/dashboard.html</a></p>
    <br>
    --
    <br>
    """ % (time_range)
    msg_alternative = MIMEMultipart('alternative')
    msg_root.attach(msg_alternative)
    msg_alternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
    base_file_name = _get_base_path() + "Figure_%d.png"
    for e in range(1, 6):
        fp = open( base_file_name % e, 'rb')
        msgImage = MIMEImage(fp.read())
        msgImage.add_header('Content-ID', '<Figure_%d>' % e)
        msg_root.attach(msgImage)
        fp.close()
    # add attachments
    csv_file_list = []
    earliest_attach_date = yesterday_date + timedelta(days=-4)
    while earliest_attach_date <= yesterday_date:
        temp_str = earliest_attach_date.strftime('%Y%m%d')
        csv_file_list.append(temp_str)
        earliest_attach_date = earliest_attach_date + timedelta(days=1)
    base_csv_file_name = _get_base_path() + "%s.csv"
    for csv_file in csv_file_list:
        csvf = open(base_csv_file_name % csv_file, 'rb')
        att = MIMEText(csvf.read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att["Content-Disposition"] = "attachment; filename=%s.csv" % csv_file
        msg_root.attach(att)
        csvf.close()
    mail_client = get_mail_client()
    try:
        all_receivers = mail_receives if len(mail_cc) == 0 else mail_receives + mail_cc
        mail_client.sendmail(mail_user, all_receivers, msg_root.as_string())
        print('sent_report_to_receives succeed')
    except smtplib.SMTPException:
        print("Error: sent_report_to_receives无法发送邮件")
    mail_client.quit()


if __name__ == '__main__':
    #sent_job_status_to_admin('20171216')
    sent_report_to_receives()
