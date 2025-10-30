import requests
import time
import hashlib
import random
import string
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def load_private_key(pem_path):
    with open(pem_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
    return private_key

def generate_nonce_str(length=32):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_signature(mchid, api_v3_key, method, url, timestamp, nonce_str, body=None,private_key_path=None):
    private_key = load_private_key(private_key_path)
    string_to_sign = f"{method}\n{url}\n{timestamp}\n{nonce_str}\n"
    if body:
        string_to_sign += body + "\n"
    string_to_sign += f"{api_v3_key}"
    signature = private_key.sign(
        string_to_sign.encode('utf-8'),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature.hex()


def sendurl(authorization,url,query_params):
    # 发送请求
    headers = {
        'Authorization': authorization,
        'Accept': 'application/json'
    }
    response = requests.get(f'https://api.mch.weixin.qq.com{url}{query_params}', headers=headers)

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")