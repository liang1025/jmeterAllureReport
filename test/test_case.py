#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 20.5.21 2:48 下午
# @Site    :
# @File    : .py
# @Software: PyCharm
import pytest
import allure
from util.xml2report import xml_2_data


class Test:

    @allure.step('用例名称:{title}')
    def title_step(self, title):
        pass

    @allure.step('请求信息')
    def request_step(self, request_url, request_header, request_data, sampler_data):
        # print(request_header)
        # print(sampler_data)
        # print(request_url)
        # print(request_data)
        pass

    @allure.step('断言信息')
    def assert_step(self, assertion_name, assertion_result):
        # print(assertion_name)
        # print(assertion_result)
        assert False

    @allure.step('文件信息:{thread}')
    def file_step(self, thread):
        pass

    @allure.step('返回信息')
    def response_step(self, status_code, status_message, response_data):
        # print(status_code, status_message, response_data)
        pass

    @allure.step('附件(全部信息)')
    def attach_all(self, data):
        allure.attach(str(data), name='attach_all_data',
                      attachment_type=allure.attachment_type.JSON)

    def base_step(self, time, date, status, title, status_code, status_message, thread, assertion_name,
                  assertion_result, response_data,
                  sampler_data, request_data, request_header,
                  request_url):
        # with allure.step('接口信息'):
        data = {'title': title, 'thread': thread, 'request_url': request_url, 'request_header': request_header,
                'request_data': request_data, 'sampler_data': sampler_data, 'status_code': status_code,
                'response_data': response_data, 'assertion_name': assertion_name, 'assertion_resul': assertion_result}
        self.file_step(thread)
        self.title_step(title)
        self.request_step(request_url, request_header, request_data, sampler_data)
        self.response_step(status_code, status_message, response_data)
        self.attach_all(data)
        if status == 'false':
            self.assert_step(assertion_name, assertion_result)
            assert False
        else:
            assert True

    @allure.title("{title}")
    @allure.feature("失败信息")
    @pytest.mark.parametrize(
        "time,date,status,story,title,status_code,status_message,thread,assertion_name,assertion_result,response_data,sampler_data,request_data,request_header,"
        "request_url",
        xml_2_data(type=1))
    def test_gjw(self, time, date, status, story, title, status_code, status_message, thread, assertion_name,
                    assertion_result,
                    response_data, sampler_data, request_data, request_header,
                    request_url):
        # allure.dynamic.story(story)
        self.base_step(time, date, status, title, status_code, status_message, thread, assertion_name, assertion_result,
                       response_data,
                       sampler_data, request_data, request_header,
                       request_url)


if __name__ == '__main__':
    pytest.main(['-s', '-q', 'D:\\learn\\pythonProject'])
