from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import requests

key = b"uah{k3y_3ncryp7_1ng_k3y}"
key = base64.b64encode(key)
key = key.ljust(32, b"=")

for i in range(10):
    resp = requests.post(
        "http://localhost:5000/api/get_signing_key",
        headers={"X-Hacker-Token": "jo7aiXieShaephaevi4Ohvengiey0kah"},
        data={"file": "testfile"},
    )
    ct = resp.json()["token"]

    ct = base64.b64decode(ct)
    iv = ct[:AES.block_size]
    ct = ct[AES.block_size:]

    cipher = AES.new(key, AES.MODE_CFB, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size).decode("UTF-8")
    print(f"{pt=}")
