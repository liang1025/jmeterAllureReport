#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/7 19:27
# @Site    :
# @File    : path_manage.py
# @Software: PyCharm
import os


class Path:
    def __init__(self):
        self.base_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

    # 获取文件的绝对路径
    # dirname :父目录  filename:文件名
    def get_real_path(self, dirname, filename):
        return os.path.join(self.base_path, dirname, filename)

    # 获取配置文件的绝对路径
    def get_config_path(self, filename):
        return os.path.join(self.base_path, 'config', filename)

    # 获取xml文件
    def get_xml_path(self, env, filename):
        return os.path.join(self.base_path, 'jmeter_result', env, filename)

    # 获取case路径
    def get_case_path(self):
        return os.path.join(self.base_path)

    # 获取case结果路径
    def get_result_path(self):
        return os.path.join(self.base_path, 'result')

    # 获取report路径
    def get_report_path(self):
        return os.path.join(self.base_path, 'report')


if __name__ == '__main__':
    path = Path()
    print(path.get_report_path())
