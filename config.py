# -*- coding:utf-8 -*-
import os
import configparser


current_dir = os.path.abspath(os.path.dirname(__file__))


class OperationalError(Exception):
    """"""


class Dictionary(dict):
    """ custom dict."""

    def __getattr__(self, key):
        return self.get(key, None)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Config:
    def __init__(self, file_name='init.conf'):
        self.env = {}
        for key, value in os.environ.items():
            self.env[key] = value

        config = configparser.ConfigParser()
        config.read(os.path.join(current_dir, file_name))

        for section in config.sections():
            setattr(self, section, Dictionary())
            for name, raw_value in config.items(section):
                try:
                    # avoid '0' and '1' to be parsed as a bool value
                    if config.get(section, name) in ['0', '1']:
                        raise ValueError
                    value = config.getboolean(section, name)
                except ValueError:
                    try:
                        value = config.getint(section, name)
                    except ValueError:
                        value = config.get(section, name)
                self.env[name] = value

    def get(self, name):
        return self.env[name]


if __name__ == "__main__":
    conf = Config()
    print(conf.get('db.qa.username'))
    print(conf.get('USERPROFILE'))
    print(conf.get('min.idle'))
    print(conf.get('db.qa.url'))




