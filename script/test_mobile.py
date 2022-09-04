import json
import logging
import unittest,requests

import app
from EncryptUtil import EncryptUtil
from api.mobileAPI import mobileAPI
from utils import encryted_Request


class testMobile(unittest.TestCase):
    def setUp(self) -> None:
        self.mobile_api = mobileAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    def test01_index(self):
        get_index_url = app.MOBILE_URL + "/phone/index/index"
        req_data = {}
        diyou = EncryptUtil.get_diyou(req_data)
        xmdy = EncryptUtil.get_xmdy(diyou)
        req_param = {"diyou":diyou,"xmdy":xmdy}
        response = requests.post(get_index_url,data=req_param)
        logging.info("response={}".format(response.json()))
        diyou_data = response.json().get("diyou")
        decryted_data = EncryptUtil.decrypt_data(diyou_data)
        data = json.loads(decryted_data)
        self.assertEqual(200,data.get("code"))
        self.assertEqual("success",data.get("result"))
#登录不成功
    def test02_login(self):
        mobile_name = "13033447711"
        pwd="test123"
        data = self.mobile_api.login(mobile_name,pwd)
        self.assertEqual(200,data.get("code"))
        self.assertEqual("success",data.get("result"))

    def test03_login(self):
        login_url = app.MOBILE_URL + "/phone/member/login"
        req_data = {"member_name": "13033447711", "password": "test123"}
        # 调用封装的发送加密数据的接口
        data = encryted_Request(login_url, req_data)
        # 对结果进行断言
        self.assertEqual(200, data.get("code"))
        self.assertEqual("success", data.get("result"))