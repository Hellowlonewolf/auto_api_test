#!/usr/bin/evn python
# -*- coding: UTF-8 -*-
# @Time    : 2019/10/12
# @Author  : zxp
import json, copy
from Base.BaseGetTestParams import del_json_value




def dictdelhead(dict, key):
    ''' 键'''
    tmp = dict.copy()
    del tmp[key]
    return tmp


def resultdata(item, res, self, params_data, ignore_key_list=[], i=None):
    """正常结果"""
    app = {}
    app["url"] = item["url"]
    app["method"] = item["method"]
    app["params"] = str(params_data)
    app["code"] = str(res.status_code)
    if i is None:
        app["msg"] = item["mark"]
    else:
        app["msg"] = "%s" % i
    app["hope"] = item.get("hope", "")
    try:
        app["res"] = json.dumps(res.json(), ensure_ascii=False)
    except:
        app["res"] = str(res.text)
    print("响应结果:%s" % app["res"])
    try:
        copy_res = copy.deepcopy(json.loads(app["res"]))
    except:
        copy_res = dict(res.headers)
        app["res"]= json.dumps(dict(res.headers), ensure_ascii=False)
    copy_hope = copy.deepcopy(json.loads(app["hope"]))
    for ignore_path in ignore_key_list:
        try:
            path_str, copy_res = del_json_value(copy_res, ignore_path)
            path_str, copy_hope = del_json_value(copy_hope, ignore_path)
        except:
            pass
    app["result"] = self(json.dumps(copy_hope, ensure_ascii=False), json.dumps(copy_res, ensure_ascii=False))
    # app["result"] = self(app["hope"], app["res"])
    print("响应码:%s" % app["code"])
    return app


def verifydata(item, res, self, params_data, ignore_key_list=[], i=None):
    """必填项缺失"""
    app = {}
    app["url"] = item["url"]
    app["method"] = item["method"]
    app["params"] = str(params_data)
    app["code"] = str(res.status_code)
    if i is None:
        app["msg"] = item["mark"]
    else:
        app["msg"] = "%s" % i
    app["hope"] = item.get("contrast", "")
    try:
        app["res"] = json.dumps(res.json(), ensure_ascii=False)
    except:
        app["res"] = str(res.text)
    print("响应结果:%s" % app["res"])
    try:
        copy_res = copy.deepcopy(json.loads(app["res"]))
    except:
        copy_res = dict(res.headers)
        app["res"]= json.dumps(dict(res.headers), ensure_ascii=False)
        app["hope"] = item.get("head_verify", "")
    copy_hope = copy.deepcopy(json.loads(app["hope"]))
    for ignore_path in ignore_key_list:
        try:
            path_str, copy_res = del_json_value(copy_res, ignore_path)
            path_str, copy_hope = del_json_value(copy_hope, ignore_path)
        except:
            pass
    app["result"] = self(json.dumps(copy_hope, ensure_ascii=False), json.dumps(copy_res, ensure_ascii=False))
    # app["result"] = self(app["hope"], app["res"])
    print("响应码:%s" % app["code"])
    return app


def nulldata(item, res, self, params_data, ignore_key_list=[], i=None):
    """值为空"""
    app = {}
    app["url"] = item["url"]
    app["method"] = item["method"]
    app["params"] = str(params_data)
    app["code"] = str(res.status_code)
    if i is None:
        app["msg"] = item["mark"]
    else:
        app["msg"] = "%s" % i
    app["hope"] = item.get("valuenull", "")
    try:
        app["res"] = json.dumps(res.json(), ensure_ascii=False)
    except:
        app["res"] = str(res.text)
    print("响应结果:%s" % app["res"])
    try:
        copy_res = copy.deepcopy(json.loads(app["res"]))
    except:
        copy_res = dict(res.headers)
        app["res"]= json.dumps(dict(res.headers), ensure_ascii=False)
        app["hope"] = item.get("head-null", "")
    copy_hope = copy.deepcopy(json.loads(app["hope"]))
    for ignore_path in ignore_key_list:
        try:
            path_str, copy_res = del_json_value(copy_res, ignore_path)
            path_str, copy_hope = del_json_value(copy_hope, ignore_path)
        except:
            pass
    app["result"] = self(json.dumps(copy_hope, ensure_ascii=False), json.dumps(copy_res, ensure_ascii=False))
    # app["result"] = self(app["hope"], app["res"])
    print("响应码:%s" % app["code"])
    return app


def typedata(item, res, self, params_data, ignore_key_list=[], i=None):
    """类型异常"""
    app = {}
    app["url"] = item["url"]
    app["method"] = item["method"]
    app["params"] = str(params_data)
    app["code"] = str(res.status_code)
    if i is None:
        app["msg"] = item["mark"]
    else:
        app["msg"] = "%s" % i
    app["hope"] = item.get("typeerr", "")
    try:
        app["res"] = json.dumps(res.json(), ensure_ascii=False)
    except:
        app["res"] = str(res.text)
    print("响应结果:%s" % app["res"])
    try:
        copy_res = copy.deepcopy(json.loads(app["res"]))
    except:
        copy_res = dict(res.headers)
        app["res"]= json.dumps(dict(res.headers), ensure_ascii=False)
        app["hope"] = item.get("head_typeerr", "")
    copy_hope = copy.deepcopy(json.loads(app["hope"]))

    for ignore_path in ignore_key_list:
        try:
            path_str, copy_res = del_json_value(copy_res, ignore_path)
            path_str, copy_hope = del_json_value(copy_hope, ignore_path)
        except:
            pass
    app["result"] = self(json.dumps(copy_hope, ensure_ascii=False), json.dumps(copy_res))
    # app["result"] = self(app["hope"], app["res"])
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
