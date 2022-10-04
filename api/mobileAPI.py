import json
import logging

import requests
import app
from EncryptUtil import EncryptUtil


class mobileAPI():
    def __init__(self):
        self.login_url = app.MOBILE_URL + "/phone/member/login"
        self.get_user_info = app.MOBILE_URL + "/phone/member/userInfo"

    def login(self,member_name,pwd):
        req_data = {"member_name":member_name,"pwd":pwd}
        diyou = EncryptUtil.get_diyou(req_data)
        xmdy = EncryptUtil.get_xmdy(diyou)

        req_param = {"diyou":diyou,"xmdy":xmdy}
        response = requests.post(self.login_url,data=req_param)

        diyou_data = response.json().get("diyou")
        data = EncryptUtil.decrypt_data(diyou_data)
        result = json.loads(data)
        return result