import json
import logging

import pymysql
import requests
from bs4 import BeautifulSoup

from EncryptUtil import EncryptUtil
import app


def assert_utils(self,response,status_code,status,desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))

def request_third_api(form_data):
    # 解析form表单中的内容，并提取第三方请求的参数
    soup = BeautifulSoup(form_data, "html.parser")
    third_url = soup.form['action']
    logging.info("third request url = {}".format(third_url))
    data = {}
    for input in soup.find_all('input'):
        data.setdefault(input['name'], input['value'])
    logging.info("third request data = {}".format(data))
    # 发送第三方请求
    response = requests.post(third_url, data=data)
    return response

class DButils():
    @classmethod
    def get_conn(cls, db_name, db_names):
        conn = pymysql.Connect(app.DB_URL,app.DB_USERNAME,app.DB_PASSWORD,db_names,autocommit = True)
        return conn
    @classmethod
    def close_conn(cls,cursor = None,conn = None):
        if cursor:cursor.close()
        if conn:conn.close()

    @classmethod
    def delete(cls,db_name,sql):
        try:
            conn=cls.get_conn(db_name)
            cursor=conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close_conn(cursor)

def read_imgVerify_data(file_name):
    file = app.BASE_DIR + "/data/" + file_name
    test_data = []
    with open(file,encoding='utf-8') as f:
        verify_data = json.load(f)
        test_data_list = verify_data.get("test_get_img_verify_code")
        for data in test_data_list:
            test_data.append((data.get("type"),data.get("status_code")))
    print("json data={}".format(test_data))
    return test_data

def read_register_data(file_name):
    file = app.BASE_DIR + "/data/" + file_name
    test_data = []
    with open(file,encoding='utf-8') as f:
        register_data = json.load(f)
        test_data_list = register_data.get("test_register")
        for data in test_data_list:
            test_data.append((data.get("phone"),data.get("pwd"),data.get('imgVerifyCode'),
                              data.get("phoneCode"),data.get("dyServer"),data.get("invite_phone"),
                              data.get("status_code"),data.get("status"),data.get("description")))
    print("json data={}".format(test_data))
    return test_data

def read_param_data(filename,method_name,param_names):
    # filename： 参数数据文件的文件名
    # method_name: 参数数据文件中定义的测试数据列表的名称，如：test_get_img_verify_code
    # param_names: 参数数据文件一组测试数据中所有的参数组成的字符串，如："type,status_code"
    file = app.BASE_DIR + "/data/" + filename
    test_case_data = []
    with open(file,encoding="utf-8") as f:
        #将json字符串转换为字典格式
        file_data = json.load(f)
        #获取所有的测试数据的列表
        test_data_list = file_data.get(method_name)
        for test_data in test_data_list:
        #先将test_data对应的一组测试数据，全部读取出来，并生成一个列表
            test_params = []
            for param in param_names.split(","):
                #依次获取同一组测试数中每个参数的值，添加到test_params中，形成一个列表
                test_params.append(test_data.get(param))
                #每完成一组测试数据的读取，就添加到test_case_data后，直到所有的测试数据读取完毕
                test_case_data.append(test_params)
    print("test_case_data = {}".format(test_case_data))
    return test_case_data

def encryted_Request(url,req_data):
    diyou = EncryptUtil.get_diyou(req_data)
    xmdy = EncryptUtil.get_xmdy(diyou)

    req_param = {"diyou": diyou, "xmdy": xmdy}
    response = requests.post(url, data=req_param)

    diyou_data = response.json().get("diyou")
    data = EncryptUtil.decrypt_data(diyou_data)
    result = json.loads(data)
    return result