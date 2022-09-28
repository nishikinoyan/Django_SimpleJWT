from Crypto import Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_cipper
from base64 import b64decode, b64encode
import redis
from SimpleJWT.settings import *

from SimpleJWT_app.encryption import key_save

# Crypto库安装
# pip install pyCryptodome
# pip install pyCrypto
# Windows下 Python\Python36\Lib\site-packages，找到这个路径，下面有一个文件夹叫做crypto,将小写c改成大写C就ok了

redis_item = redis.Redis(host=redis_host, port=redis_port)


def create_key():
    '''
    redis_item.set('pub_key', public)
    redis_item.set('pri_key', private)
    '''
    random_generator = Random.new().read
    rsa = RSA.generate(1024, random_generator)
    private = rsa.exportKey().decode('utf-8')
    public = rsa.publickey().exportKey().decode('utf-8')
    key_save.public_key = public
    key_save.private_key = private


def decrypt_data_on_private(content):
    random_generator = Random.new().read
    private_key = RSA.importKey(key_save.private_key)
    cipher = PKCS1_v1_5_cipper.new(private_key)
    decrypt_data = cipher.decrypt(b64decode(content), random_generator)
    return decrypt_data.decode('utf-8')


def encrypt_date_on_public(content):
    public_key = RSA.importKey(key_save.public_key)
    cipher = PKCS1_v1_5_cipper.new(public_key)
    encrypt_data = b64encode(cipher.encrypt(bytes(content.encode('utf-8'))))
    return encrypt_data.decode('utf-8')