#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 22.5.21 6:52 下午
# @Site    :
# @File    : report_edit.py
# @Software: PyCharm
from util.path_manage import Path
import os
import json
from util.xml2report import xml_2_data

result = xml_2_data()


def report_edit(env):
    path = os.path.join(Path().get_report_path(), env, 'data')
    # 批量更新聚合文件
    for file in os.listdir(path):
        if '.json' in file and 'categories' not in file:
            try:
                with open(os.path.join(path, file), 'r') as f:
                    json_str = json.loads(f.read())
                    for data in json_str['children'][0]['children']:
                        name = data['name']
                        for meta in result:
                            if name == meta[3]:
                                data['time']['start'] = int(meta[1])
                                data['time']['stop'] = int(meta[1]) + int(meta[0])
                                data['time']['duration'] = int(meta[0])
                    with open(os.path.join(path, file), 'w') as w:
                        json.dump(json_str, w, indent=2, sort_keys=True, ensure_ascii=False)
            except Exception as e:
                print(e)
    # 批量更新case文件
    cases_path = os.path.join(path, 'test-cases')
    for file in os.listdir(cases_path):
        if '.json' in file and 'categories' not in file:
            try:
                with open(os.path.join(cases_path, file), 'r') as f:
                    json_str = json.loads(f.read())
                    name = json_str['name']
                    for meta in result:
                        if name == meta[3]:
                            json_str['time']['start'] = int(meta[1])
                            json_str['time']['stop'] = int(meta[1]) + int(meta[0])
                            json_str['time']['duration'] = int(meta[0])
                    with open(os.path.join(cases_path, file), 'w') as w:
                        json.dump(json_str, w, indent=2, sort_keys=True, ensure_ascii=False)
            except Exception as e:
                print(e)
