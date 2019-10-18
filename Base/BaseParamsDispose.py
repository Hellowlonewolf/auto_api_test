#!/usr/bin/evn python
# -*- coding: UTF-8 -*-
# @Time    : 2019/10/12
# @Author  : zxp
import  copy
import requests
import json
import json_tools
import ast
from Base.BaseElementEnmu import Element
from Base.BaseStatistics import writeInfo
from Base.BaseGetTestParams import get_test_data,  update_json_data_unique, del_json_value

class sendmethod():
    def __init__(self,test_case_count):
        self.test_case_count=test_case_count
    def post_data_normal(self, url, header, item, unique_flag, ignore_key_list):
        # 正向请求
        post_data = ast.literal_eval(item["params"])
        post_data = update_json_data_unique(post_data, unique_flag)
        if item["method"] == "get":
            res = requests.get(url, json=post_data, headers=header, verify=False)
        elif item["method"] == "post":
            res = requests.post(url, json=post_data, headers=header,
                                verify=False)
        else:
            print("现在只针post和get方法进行了测试，其他方法请自行扩展")
        writeInfo(resultdata(item, res, self.__verify, post_data, "hope", ignore_key_list), Element.INFO_FILE)
        self.test_case_count += 1

    def post_data_more(self, url, header, item, unique_flag, ignore_key_list):

        # 参数多传请求
        post_more_data = ast.literal_eval(item["params"])
        post_more_data = update_json_data_unique(post_more_data, unique_flag)
        post_more_data.update({"more": 12345})
        if item["method"] == "get":
            res = requests.get(url, json=post_more_data, headers=header, verify=False)
        elif item["method"] == "post":
            res = requests.post(url, json=post_more_data, headers=header,
                                verify=False)
        else:
            print("现在只针post和get方法进行了测试，其他方法请自行扩展")
        writeInfo(resultdata(item, res, self.__verify, post_more_data, "hope", ignore_key_list, "参数多传"),
                  Element.INFO_FILE)
        self.test_case_count += 1

    def post_data_header_error(self, url, header, item, unique_flag):
        # 请求头
        if item["head_required"] != "":
            for z in ast.literal_eval(item["head_required"]):
                for i in ast.literal_eval(str(header)):
                    post_data = ast.literal_eval(item["params"])
                    post_data = update_json_data_unique(post_data, unique_flag)
                    header_data = dictdelhead(header, i)
                    header_data = update_json_data_unique(header_data, unique_flag)
                    res = requests.post(url, json=post_data, headers=header_data,
                                        verify=False)
                    writeInfo(verifyhead(item, res, self.__verify, header_data, z, i), Element.INFO_FILE)
                    self.test_case_count += 1
        else:
            pass

    def post_data_error(self, url, header, paths, item, required_key_list, unique_flag, ignore_key_list):
        global test_case_count
        for i in paths:
            if i in required_key_list:
                required_flag = True
            else:
                required_flag = False
            # 生成参数异常测试数据（1、参数缺失（不填）， 2、为空， 3、类型异常）
            params = get_test_data(ast.literal_eval(item["params"]), i, required_flag, unique_flag)
            for i in params:
                _info = ""
                if i.get("info", "null") != "null":
                    _info = i.get("info", "参数正确")
                    info = i.pop("info")
                if item["method"] == "get":
                    res = requests.get(url, data=json.dumps(i), headers=header)
                else:
                    res = requests.post(url, data=json.dumps(i), headers=header)

                if "非必填项 参数值为空" in info or "非必填项 参数缺失" in info:
                    writeInfo(resultdata(item, res, self.__verify, i, "hope", ignore_key_list, info), Element.INFO_FILE)
                elif "必填项 参数缺失" in info:
                    writeInfo(resultdata(item, res, self.__verify, i, "contrast", ignore_key_list, "head_verify", info),
                              Element.INFO_FILE)
                elif "必填项 参数值为空" in info:
                    writeInfo(resultdata(item, res, self.__verify, i, "valuenull", ignore_key_list, "head-null", info),
                              Element.INFO_FILE)
                elif "参数类型异常" in info:
                    writeInfo(resultdata(item, res, self.__verify, i, "typeerr", ignore_key_list, "head_typeerr", info),
                              Element.INFO_FILE)
                self.test_case_count += 1

    def __verify(self, hope, res):
        """
        比对实际结果与预期结果
        """
        contrast_data = json.loads(hope)
        res_data = json.loads(res)
        json_tool_res = json_tools.diff(contrast_data, res_data)
        if json_tool_res == []:
            return "通过"
        else:
            return "失败"

    def check_type(self, param):
        """
        检查随机数参数的类型，用于生成相同类型的随机数
        """
        if isinstance(param, int):
            typ = "int"
        elif isinstance(param, str):
            typ = "str"
        elif isinstance(param, float):
            typ = "float"
        else:
            typ = None
        return typ

    def set_unique_params(self, item):
        """
        将随机参数存到字典中
        """
        unique_flag = {}
        if item["unique_params"] != "":
            for un in ast.literal_eval(item["unique_params"]):
                param = eval(item["params"])
                unique_flag.update({un: self.check_type(param[un])})
        return unique_flag








def dictdelhead(dict, key):
    ''' 键'''
    tmp = dict.copy()
    del tmp[key]
    return tmp


def resultdata(item, res, self, params_data, verifytype, ignore_key_list=[], verifyhead=None, i=None):
    """结果验证"""
    app = {}
    app["url"] = item["url"]
    app["method"] = item["method"]
    app["params"] = str(params_data)
    app["code"] = str(res.status_code)
    if i is None:
        app["msg"] = item["mark"]
    else:
        app["msg"] = "%s" % i
    app["hope"] = item.get(verifytype, "")
    try:
        app["res"] = json.dumps(res.json(), ensure_ascii=False)
    except:
        app["res"] = str(res.text)
    print("响应结果:%s" % app["res"])
    try:
        copy_res = copy.deepcopy(json.loads(app["res"]))
    except:
        copy_res = dict(res.headers)
        app["res"] = json.dumps(dict(res.headers), ensure_ascii=False)
        app["hope"] = item.get(verifyhead, "")
    copy_hope = copy.deepcopy(json.loads(app["hope"]))
    for ignore_path in ignore_key_list:
        try:
            path_str, copy_res = del_json_value(copy_res, ignore_path)
            path_str, copy_hope = del_json_value(copy_hope, ignore_path)
        except:
            pass
    app["result"] = self(json.dumps(copy_hope, ensure_ascii=False), json.dumps(copy_res, ensure_ascii=False))
    print("响应码:%s" % app["code"])
    return app


def verifyhead(item, res, self, params_data, head, i=None):
    app = {}
    app["url"] = item["url"]
    app["method"] = item["method"]
    app["params"] = str(params_data)
    app["code"] = str(res.status_code)
    if head == i:
        app["msg"] = "必填项头缺失:['%s']" % i
        app["hope"] = item.get("head_verify", "")
    else:
        app["msg"] = "非必填项头缺失:['%s']" % i
        app["hope"] = item.get("hope", "")
    try:
        app["res"] = json.dumps(res.json(), ensure_ascii=False)
    except:
        app["res"] = str(res.text)
    print("响应结果:%s" % app["res"])
    app["result"] = self(app["hope"], app["res"])
    print("响应码:%s" % app["code"])
    return app
