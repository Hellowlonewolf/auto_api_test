from Base.BaseRunner import ParametrizedTestCase
from Base.BaseGetExcel import read_excel
from Base.BaseReq import Config
from Base.BaseElementEnmu import Element


class ApiTest(ParametrizedTestCase):
    def test_api(self):
        ls = read_excel(Element.API_FILE)
        Config().config_req(ls)

    @classmethod
    def setUpClass(cls):
        super(ApiTest, cls).setUpClass()
        # cls.req
