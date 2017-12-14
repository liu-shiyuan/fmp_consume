# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import urllib.parse
from config import Config

mpl.rcParams['font.sans-serif'] = ['SimHei']
c = Config()
url = urllib.parse.urljoin(c.get('domain'), c.get('api'))
print(url)
dest_url = urllib.parse.urljoin(url, '2017-05-99')
print(dest_url)