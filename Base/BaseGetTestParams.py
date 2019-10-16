# -*-coding:UTF-8 -*-
# @Time    : 2019-10-14 14:28:12
# @Author  : lsf
# 生成测试用例，参数 1、参数缺失（不填）， 2、为空， 3、异常类型

import copy
import string
import random
import collections

from collections.abc import Iterable


def get_null_value_list(value):
    """
    构造空数据
    """
    if isinstance(value, str):
        return ["", None]
    elif isinstance(value, int):
        return [None]
    elif isinstance(value, list):
        return [[], None]
    elif isinstance(value, tuple):
        return [(), None]
    elif isinstance(value, dict):
        return [{}, None]
    else:
        return [None]


def get_other_type_list(value):
    """
    构造不正确的value类型
    """
    if isinstance(value, str):
        return [1, ["str"], {"str": "str"}]
    elif isinstance(value, int):
        return ["1", ["1"], {"int": 1}]
    elif isinstance(value, list):
        return ["1", 1, {"list": ["list"]}]
    elif isinstance(value, tuple):
        return ["1", 1, {"tuple": ["tuple"]}]
    elif isinstance(value, dict):
        return ["1", 1, [{"dict": "dict"}]]
    else:
        return [None]


def get_paths(source):
    '''
    遍历json，获取所有key路径list
    :param source:
    :return:
    '''
    paths = []
    if isinstance(source, collections.abc.MutableMapping):  # found a dict-like structure...
        for k, v in source.items():  # iterate over it; Python 2.x: source.iteritems()
            paths.append([k])  # add the current child path
            paths += [[k] + x for x in get_paths(v)]  # get sub-paths, extend with the current
    # else, check if a list-like structure, remove if you don't want list paths included
    elif isinstance(source, collections.abc.Sequence) and not isinstance(source, str):
        #                          Python 2.x: use basestring instead of str ^
        for i, v in enumerate(source):
            paths.append([i])
            paths += [[i] + x for x in get_paths(v)]  # get sub-paths, extend with the current
    return paths


def get_json_value(json_data, p_l):
    '''
    根据key路径list，获取值
    :param p_l:
    :param v:
    :return:
    '''
    path_str = ""
    for k in p_l:
        if isinstance(k, str): path_str += "['" + k + "']"
        if isinstance(k, int): path_str += "[" + str(k) + "]"
    return path_str, eval("json_data" + path_str)


def set_json_value(json_data, p_l, v):
    '''
    根据key路径list，更新值为v
    :param json_data:
    :param p_l:
    :param v:
    :return:
    '''
    update_json = copy.deepcopy(json_data)
    path_str = ""
    for k in p_l:
        if isinstance(k, str): path_str += "['" + k + "']"
        if isinstance(k, int): path_str += "[" + str(k) + "]"
    exec("update_json" + path_str + " = v")
    # exec("del update_json" + path_str)
    return path_str, update_json


def del_json_value(json_data, p_l):
    '''
    根据key路径list，删除key
    :param json_data:
    :param p_l:
    :param v:
    :return:
    '''
    update_json = copy.deepcopy(json_data)
    path_str = ""
    for k in p_l:
        if isinstance(k, str): path_str += "['" + k + "']"
        if isinstance(k, int): path_str += "[" + str(k) + "]"
    exec("del update_json" + path_str)
    return path_str, update_json


def random_str(random_length=10):
    """
    生成一个指定长度的随机字符串
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(random_length)]
    random_str = ''.join(str_list)
    return random_str


def update_json_data_unique(json_data, unique_flag):
    if unique_flag != {}:
        for key in unique_flag:
            if unique_flag[key] == "int":
                json_data[key] = random.randint(0, 900000)
            elif unique_flag[key] == "str":
                json_data[key] = random_str()
    return json_data


def get_test_data(json_data, path_list, required_flag, unique_flag):
    '''
    根据key路径list，修改value
    '''
    data_update = copy.deepcopy(json_data)
    data_update = update_json_data_unique(data_update, unique_flag)
    test_param_lsit = []
    path_str, value = get_json_value(data_update, path_list)
    if required_flag:
        required_flag_str = "必填项"
    else:
        required_flag_str = "非必填项"
    print("=" * 20, required_flag_str, path_str, "=" * 20)
    # print("get: %s \ndata: %s" % (path_str, json.dumps(value)))
    path_str, update_json = del_json_value(data_update, path_list)
    # print("删除参数, data: %s" % (json.dumps(update_json)))
    copy_test_param = copy.deepcopy(update_json)
    copy_test_param["info"] = required_flag_str + ' 参数缺失: ' + path_str
    test_param_lsit.append(copy_test_param)
    null_value_list = get_null_value_list(value)
    for n in null_value_list:
        data_update = update_json_data_unique(data_update, unique_flag)
        path_str, update_json = set_json_value(data_update, path_list, n)
        # print("参数值为空, data: %s" % (json.dumps(update_json)))
        copy_test_param = copy.deepcopy(update_json)
        copy_test_param["info"] = required_flag_str + ' 参数值为空: ' + path_str
        test_param_lsit.append(copy_test_param)
    error_type_list = get_other_type_list(value)
    for e in error_type_list:
        data_update = update_json_data_unique(data_update, unique_flag)
        path_str, update_json = set_json_value(data_update, path_list, e)
        # print("参数类型异常, data: %s" % (json.dumps(update_json)))
        copy_test_param = copy.deepcopy(update_json)
        copy_test_param["info"] = '参数类型异常: ' + path_str
        test_param_lsit.append(copy_test_param)
    return test_param_lsit

