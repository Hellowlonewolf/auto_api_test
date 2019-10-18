import requests
import json
import json_tools
import ast
from Base.BaseElementEnmu import Element
from Base.BaseParamsDispose import  sendmethod
from Base.BaseGetTestParams import  get_paths


class Config(sendmethod):
    def __init__(self, test_case_count):
        sendmethod.__init__(self, test_case_count)
        self.test_case_count = test_case_count

    def config_req(self, kw):
        """
        设置接口请求数据各种情况，生成测试用例
        1，参数设置；2，生成测试用例并将结果写入excel
        """
        header = {}
        for item in kw:
            # 参数处理
            url = "%s://%s" % (item["protocol"], item["url"])
            # 请求头设置
            if item["head_required"] != "":
                head = item['header']
                header = eval(head)
            # 需要随机请求的参数
            unique_flag = self.set_unique_params(item)
            # 获取必填参数路径
            required_key_list = []
            if item["required"] != "":
                for r in ast.literal_eval(item["required"]):
                    key_path = r.split(".")
                    for i in range(len(key_path)):
                        try:
                            key_path[i] = int(key_path[i])
                        except:
                            pass
                    required_key_list.append(key_path)
            # 获取忽略响应结果校验参数路径
            ignore_key_list = []
            if item["ignore"] != "":
                for r in ast.literal_eval(item["ignore"]):
                    key_path = r.split(".")
                    for i in range(len(key_path)):
                        try:
                            key_path[i] = int(key_path[i])
                        except:
                            pass
                    ignore_key_list.append(key_path)
            # 获取所有参数key的路径
            paths = get_paths(ast.literal_eval(item["params"]))

            # 生成测试用例并将结果写入excel
            # 正向请求
            self.post_data_normal(url, header, item, unique_flag, ignore_key_list)
            # 请求头异常
            self.post_data_header_error(url, header, item, unique_flag)
            # 参数异常
            self.post_data_error(url, header, paths, item, required_key_list, unique_flag, ignore_key_list)
            # 参数多传
            self.post_data_more(url, header, item, unique_flag, ignore_key_list)
        Element.TEST_CASE = self.test_case_count
