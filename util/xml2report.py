#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19.5.21 2:37 下午
# @Site    :
# @File    : xml2report.py
# @Software: PyCharm
"""
t表示从请求开始到响应结束的时间：time
lt表示整个的空闲时间
ts表示访问的时刻: date
s表示返回的结果true表示成功，false表示失败:status
lb表示标题:title
rc表示返回的响应码:status_code
rm表示响应信息:status_message
tn表示线程的名字“1-138”表示第1个线程组的第138个线程。:thread
dt表示响应的文件类型
by表示请求和响应的字节数
"""
import xmltodict
import pytest
import json
from datetime import datetime
from util.path_manage import Path
from util.file_manage import YamlManage
import re


def xml_2_data(type: int = 1):
    env = YamlManage('config.yml').get_data('env')

    result_file = open(Path().get_xml_path(env, 'result.xml'.format(env, int(type))), "r", encoding='utf-8').read()

    try:
        converte_data = xmltodict.parse(result_file, encoding='utf-8')
        # converte_data = xml2json.xml2json(result_file)
        sample_keys = list(converte_data['testResults'].keys())
        result = []
        ws_result = []
        sample_result = converte_data['testResults']['httpSample'] if isinstance(
            converte_data['testResults']['httpSample'],
            list) else [converte_data['testResults']['httpSample']]
        if 'sample' in sample_keys:
            ws_result = converte_data['testResults']['sample'] if isinstance(converte_data['testResults']['sample'],
                                                                             list) else [
                converte_data['testResults']['sample']]
        result_data = sample_result + ws_result
        for data in result_data:
            time = data['@t'] if '@t' in data else ''
            date = data['@ts'] if '@ts' in data else ''
            # date = datetime.fromtimestamp(data['@ts']/1000).strftime("%Y:%m:%d %H:%M:%S") if '@ts' in data else None
            # status用例运行断言 成功 or 失败
            status = data['@s'] if '@s' in data else ''
            title = data['@lb'] if '@lb' in data else ''
            # status_code=200
            status_code = data['@rc'] if '@rc' in data else ''
            status_message = data['@rm'] if '@rm' in data else ''
            thread = data['@tn'] if '@tn' in data else ''
            assertion = data['assertionResult'] if 'assertionResult' in data else ''
            response_data = data['responseData']['#text'] if 'responseData' in data and '#text' in data['responseData'] \
                else ''
            sampler_data = data['samplerData']['#text'] if 'samplerData' in data and '#text' in data['samplerData'] \
                else ''
            request_data = data['queryString']['#text'] if 'queryString' in data and '#text' in data[
                'queryString'] else ''
            request_header = data['requestHeader']['#text'] if 'requestHeader' in data and '#text' in data[
                'requestHeader'] else ''
            request_url = data['java.net.URL'] if 'java.net.URL' in data else ''
            story = '未标记'
            assertion_name, assertion_result = None, None
            if status == 'false':
                assertion_name, assertion_result = get_assertion(assertion)
                # data = {'title': title, 'thread': thread, 'request_url': request_url, 'request_header': request_header,
                #         'request_data': request_data, 'sampler_data': sampler_data, 'status_code': status_code,
                #         'response_data': response_data, 'assertion_name': assertion_name,
                #         'assertion_result': assertion_result
                #         }
                # story = set_fail_tag(data)

            meta_data = (
                time, date, status, story, title, status_code, status_message, thread, assertion_name, assertion_result,
                response_data
                , sampler_data, request_data, request_header, request_url)
            # meta_data = (title,assertion_result)
            result.append(meta_data)
        return result
    except Exception as e:
        print(e)
        return [
            ('time', 'date', 'true', 'story', 'title', 'status_code', 'status_message', 'thread', 'assertion_name',
             'assertion_result',
             'response_data', 'sampler_data', 'request_data', 'request_header', 'request_url')]


def get_assertion(assertion):
    assertion_name, assertion_result = None, None
    if isinstance(assertion, list):
        for value in assertion:
            if 'failureMessage' in value and value['failureMessage'] is not None:
                assertion_result = value['failureMessage']
                assertion_name = value['name']
                break
    elif isinstance(assertion, dict):
        if 'failureMessage' in assertion and assertion['failureMessage'] is not None:
            assertion_result = assertion['failureMessage']
            assertion_name = assertion['name']
    return assertion_name, assertion_result


def set_fail_tag(data):
    # [('name', '响应断言'), ('failure', 'false'), ('error', 'false')])
    config = YamlManage('fail_analysis_cfg.yml').get_data('config')

    story = '未标记'
    for c1 in config:
        matches = c1.get('match_regex')
        is_matched = False
        for match in matches:
            is_matched = is_matched and do_match(match)  # 不同key之间 且
        if is_matched:  # 如果匹配到 则退出循环 当前case标记成功，如果没有 继续下一个配置对比
            story = c1.get('fail_type_desc')
            break
    return story


def do_match(data, match):
    key = match.get('key')
    values = match.get('values')
    is_matched = False
    if len(values) <= 0:
        return True
    for v in values:
        if re.search(v, data.get(key), flags=0) != None:
            is_matched = True  # values中的匹配 或关系
            break
    return is_matched


if __name__ == '__main__':
    print(xml_2_data(5))
