# -*- coding:utf-8 -*-
import os
import platform


def determine_default_file_path(file_name, file_ext):
    _check_path()
    return _get_base_path() + file_name + '.' + file_ext


def _get_base_path():
    if 'windows' == platform.system().lower():
        base_path = os.getenv('USERPROFILE')
    elif 'linux' == platform.system().lower():
        base_path = os.getenv('HOME')
    elif 'darwin' == platform.system().lower():
        base_path = os.getenv('HOME') # ??? 太穷没有mac测试
    return base_path + '/fmp_consume/'


def _not_exits_to_mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def _check_path():
    base_path = _get_base_path()
    _not_exits_to_mkdir(base_path)


if __name__ == '__main__':
    print(determine_default_file_path('21075555', 'csv'))