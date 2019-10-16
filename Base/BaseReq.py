import requests
import json
import json_tools
import ast
from Base.BaseElementEnmu import Element
from Base.BaseStatistics import writeInfo
from Base.BaseParamsDispose import dictdelhead, resultdata, verifydata, nulldata, typedata,verifyhead
from Base.BaseGetTestParams import get_test_data, get_paths, update_json_data_unique

test_case_count = 2


class Config(object):
    def __init__(self):
        pass

    def config_req(self, kw):
        """
        正向请求，请求头异常情况
        """
        global test_case_count
        header = {}
        for item in kw:
            url = "%s://%s" % (item["protocol"], item["url"])
            print("请求url:%s " % url)
            print("请求参数:%s" % item["params"])
            # 请求头设置
            if item["head_required"] != "":
                head = item['header']
                header = eval(head)
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
            # 需要随机请求的参数
            unique_flag = self.set_unique_params(item)
            # 正向请求
            post_data = ast.literal_eval(item["params"])
            post_data = update_json_data_unique(post_data, unique_flag)
            # 参数多传请求
            post_more_data = ast.literal_eval(item["params"])
            post_more_data = update_json_data_unique(post_more_data, unique_flag)
            post_more_data.update({"more": 12345})
            data_list = [post_data, post_more_data]
            for data in data_list:
                if item["method"] == "get":
                    res = requests.get(url, json=data, headers=header, verify=False)
                elif item["method"] == "post":
                    res = requests.post(url, json=data, headers=header,
                                        verify=False)
                else:
                    print("现在只针post和get方法进行了测试，其他方法请自行扩展")
                test_case_count += 1
                if len(data) > len(ast.literal_eval(item["params"])):
                    writeInfo(resultdata(item, res, self.__verify, data, ignore_key_list, "参数多传"), Element.INFO_FILE)
                else:
                    writeInfo(resultdata(item, res, self.__verify, data, ignore_key_list), Element.INFO_FILE)
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
                        test_case_count += 1
            else:
                pass
        self.config_req_pict(kw)

    def config_req_pict(self, kw):
        """
        参数异常请求
        """
        global test_case_count
        header = {}
        for item in kw:
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
            # 获取所有key的路径
            paths = get_paths(ast.literal_eval(item["params"]))

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
                        writeInfo(resultdata(item, res, self.__verify, i, ignore_key_list, info), Element.INFO_FILE)
                    elif "必填项 参数缺失" in info:
                        writeInfo(verifydata(item, res, self.__verify, i, ignore_key_list, info), Element.INFO_FILE)
                    elif "必填项 参数值为空" in info:
                        writeInfo(nulldata(item, res, self.__verify, i, ignore_key_list, info), Element.INFO_FILE)
                    elif "参数类型异常" in info:
                        writeInfo(typedata(item, res, self.__verify, i, ignore_key_list, info), Element.INFO_FILE)
                    test_case_count += 1

        Element.TEST_CASE = test_case_count

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
        unique_flag = {}
        if item["unique_params"] != "":
            for un in ast.literal_eval(item["unique_params"]):
                param = eval(item["params"])
                unique_flag.update({un: self.check_type(param[un])})
        return unique_flag




