import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class Element(object):
    INFO_FILE = PATH("../Log/info.pickle")  # 记录结果
    REPORT_FILE = PATH("../Report/Report.xlsx")  # 测试报告
    API_FILE = PATH("../Report/api.xlsx")  # 用例文件

    TEST_CASE = 10000
