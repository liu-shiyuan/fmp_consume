import time, datetime

unix_time_2_time = time.localtime(1510798263)
f = '%Y/%m/%d %H:%M:%S'
a = time.strftime(f, unix_time_2_time)

temp = 'sff-fdfdjff-f-ff'
temp = temp.replace('-', '/')
print(temp)