import base64
import binascii
import json
import os

from Crypto.Cipher import AES

from api.netease import config


def create_secret_key(a):
    """
    生成一个随机字符串
    :param a: 字符串长度
    :return: 随机字符串
    """
    return binascii.hexlify(os.urandom(a))[:16]


def aes_encrypt(text, sec_key):
    """
    aes 加密
    :param text: 要加密的文本
    :param sec_key: 私钥
    :return: 加密后的文本
    """
    pad = 16 - len(text) % 16
    text = text + chr(pad) * pad
    iv = "0102030405060708"
    encryptor = AES.new(sec_key, AES.MODE_CBC, iv)
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return ciphertext


def rsa_encrypt(text, pub_key, modulus):
    """
    RSA 加密采用非常规填充方式，网易是直接向前补0
    :param text: 要加密文本
    :param pub_key: 公钥
    :param modulus: 加密系数
    :return: 加密后字符串
    """
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16), int(pub_key, 16), int(modulus, 16))
    return format(rs, 'x').zfill(256)


def encrypted_request(text):
    """
    对请求进行加密
    :param text: 要加密的请求参数
    :return: 加密后的 post data
    """
    text = json.dumps(text)
    sec_key = create_secret_key(16)
    enc_text = aes_encrypt(aes_encrypt(text, config.nonce), sec_key)
    enc_sec_key = rsa_encrypt(sec_key, config.pub_key, config.modulus)
    return {'params': enc_text, 'encSecKey': enc_sec_key}
