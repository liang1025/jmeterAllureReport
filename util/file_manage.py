#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/2 9:55
# @Site    :
# @File    : file_manage.py
# @Software: PyCharm
import os
import yaml
from util.path_manage import Path


class YamlManage:
    def __init__(self, filename):
        if os.path.exists(Path().get_config_path(filename)):
            self.yaml_file = Path().get_config_path(filename)
        else:
            raise FileNotFoundError("配置文件不存在")
        self._data = None

    @property
    def data(self):
        if not self._data:
            with open(self.yaml_file, 'rb') as f:
                self._data = list(yaml.unsafe_load_all(f))
        return self._data

    def get_data(self, element):
        value = self.data[0].get(element)
        if value == None:
            for key, value in self.data[0].items():
                while (type(value) == dict):
                    return value.get(element)
        return value

    def set_data(self, key, value):
        data = self.data[0]
        data[key] = value
        with open(self.yaml_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, encoding='utf-8', allow_unicode=True)


if __name__ == '__main__':
    config = YamlManage('config.yml')
    print(config.get_data('env'))
