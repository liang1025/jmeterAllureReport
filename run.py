#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/27 13:50
# @Site    :
# @File    : run.py
# @Software: PyCharm
import pytest
import time
import sys
import os
import shutil
from util.path_manage import Path
from util.xml2report import xml_2_data
from util.report_edit import report_edit
from util.file_manage import YamlManage

result = xml_2_data()

# case 路径
CASE_DIR = Path().get_case_path()

# result 路径
RESULT_DIR = Path().get_result_path()
# report路径
REPORT_DIR = Path().get_report_path()

if __name__ == '__main__':
    # now = time.strftime("%Y%m%d%H%M%S")
    env = YamlManage('config.yml').get_data('env')
    # 更新配置文件
    YamlManage('config.yml').set_data('env', env)
    pytest.main(['-s', '-q', '--cache-clear', os.path.join(CASE_DIR, env), '--clean-alluredir', '--alluredir',
                 os.path.join(RESULT_DIR, 'result-{0}'.format(env))])

    shutil.copyfile(os.path.join(RESULT_DIR, 'environment_{}.properties'.format(env)),
                    os.path.join(RESULT_DIR, 'result-{0}'.format(env), 'environment.properties'))

    shutil.copyfile(os.path.join(RESULT_DIR, 'categories.json'),
                    os.path.join(RESULT_DIR, 'result-{0}'.format(env), 'categories.json'))
    # shutil.copytree(REPORT_DIR,os.path.join(CASE_DIR,'report_bak','report-{}'.format(now)))
    allurePath = os.path.join(RESULT_DIR, 'result-{}'.format(env))
    os.chdir(allurePath)
    os.system('allure generate --clean ' + allurePath)
    # 处理报告文件中case时间与实际执行时间保持一致
    report_edit(env)