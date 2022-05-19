import base64
import hashlib
import json
import re
import traceback

from Crypto.Cipher import AES


# 加解密工具类
class EncryptUtil:
    # 发送请求时，加密密码
    SEND_AES_KEY = ";3jm$>/p-ED^cVz_j~.KV&V)k9jn,UAH"
    # 发送请求时，签名密钥
    SEND_SIGN_KEY = "DY34fdgsWET@#$%wg#@4fgd345sg"
    # 接收数据时，解密密钥
    RECEIVE_AES_KEY = "54Ms5bkE6UEdyrRviJ0![OR]g+i79x]k"

    @staticmethod
    def padding_pkcs5(value):
        BS = AES.block_size
        return str.encode(value + (BS - len(value) % BS) * chr(BS - len(value) % BS))

    # 替换空字符
    @staticmethod
    def replace_blank(str_data):
        str_data = re.compile("\t|\r|\n").sub("", str_data)
        print("replace_blank str_data=", str_data)
        return str_data

    @staticmethod
    def aes_encrypt(key, data):
        """
        AES加密
        :param key: 密钥
        :param data: 待加密数据
        :return: 加密后数据
        """
        data = base64.encodebytes(data.encode()).decode()
        # 替换特殊字符
        data = EncryptUtil.replace_blank(data)
        print("data=", data)

        # 初始化加密器
        aes = AES.new(key.encode(), AES.MODE_ECB)

        # 加密
        padding_value = EncryptUtil.padding_pkcs5(data)
        encrypt_aes = aes.encrypt(padding_value)

        # 用base64转成字符串形式
        encrypted_text = base64.encodebytes(encrypt_aes).decode()
        return encrypted_text

    @staticmethod
    def aes_decrypt(key, data):
        """
        AES解密
        :param key: 密钥
        :param data: 待解密数据
        :return: 解密后数据
        """
        # 初始化加密器
        aes = AES.new(key.encode(), AES.MODE_ECB)
        # 优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(data.encode())

        # 执行解密
        decrypted_bytes = base64.decodebytes(aes.decrypt(base64_decrypted))
        # 转换为字符串
        decrypted_text = str(decrypted_bytes, encoding="utf-8")

        # 把Unicode转成中文
        result = decrypted_text.encode().decode("unicode_escape")
        return result

    @staticmethod
    def md5value(data):
        print("md5value data=", data)
        md5 = hashlib.md5()
        md5.update(data.encode())
        return md5.hexdigest()

    # 加密调用
    @staticmethod
    def get_diyou(data):
        # 把字典转换为JSON字符串
        if isinstance(data, dict):
            data = json.dumps(data)
        aes_encrypt_data = EncryptUtil.aes_encrypt(EncryptUtil.SEND_AES_KEY, data)
        return EncryptUtil.replace_blank(aes_encrypt_data)

    # 签名调用
    @staticmethod
    def get_xmdy(data):
        return EncryptUtil.md5value(
            EncryptUtil.SEND_SIGN_KEY + EncryptUtil.replace_blank(data) + EncryptUtil.SEND_SIGN_KEY)

    # 解密调用
    @staticmethod
    def decrypt_data(data):
        return EncryptUtil.aes_decrypt(EncryptUtil.RECEIVE_AES_KEY, data)


if __name__ == '__main__':
    # 加密
    send_data = {}
    content = json.dumps(send_data)
    diyou = EncryptUtil.get_diyou(content)
    print("diyou=", diyou)
    xmdy = EncryptUtil.get_xmdy(diyou)
    print("xmdy=", xmdy)

