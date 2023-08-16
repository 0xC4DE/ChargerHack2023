import os
import sys
import subprocess
import datetime

from Crypto.Cipher import AES
import base64

from Crypto.Util.Padding import unpad

DIR = "veryspecificdir"
FILE = DIR + os.path.sep + "test{}.txt"
ENCRYPTED_FILE = DIR + os.path.sep + "encrypted_test{}.txt.enc"


def create_enc():
    os.makedirs(DIR, exist_ok=True)
    for x in range(3):
        if os.path.exists(ENCRYPTED_FILE.format(x)):
            os.remove(ENCRYPTED_FILE.format(x))
        with open(FILE.format(x), "w") as f:
            f.write("1234567890123456")

    p = subprocess.Popen(("./chrometokenmanager"))
    p.wait()

    for x in range(3):
        if not os.path.isfile(ENCRYPTED_FILE.format(x)):
            raise Exception("encrypted file wasn't made for some reason")


def try_dec(before_uuid_pref, after_uuid_pref):
    ct = open(ENCRYPTED_FILE.format(1), "rb").read()
    print(f"{ct=}")
    print(f"{len(ct)=}")

    iv = ct[:16]
    ct = ct[16:]
    #ct = ct[AES.block_size :]

    for uuid_first in range(before_uuid_pref, after_uuid_pref):
        uuid = str(hex(uuid_first)[2:]) + "-3c70-11ee-8045-7c5079e75ea0"
        print(uuid[:16])
        cipher = AES.new(uuid[:16].encode("utf-8"), AES.MODE_CFB, iv, segment_size=128)
        try:
            pt = cipher.decrypt(ct).decode("utf-8")
        except Exception as e:
            continue

        print(f"{uuid=} {pt=}")

def decrypt_encrypted_key(ct, key=None):
    key = b"uah{k3y_3ncryp7_1ng_k3y}"
    key = base64.b64encode(key)
    key = key.ljust(32, b"=")

    ct = base64.b64decode(ct)
    iv = ct[:AES.block_size]
    ct = ct[AES.block_size:]

    cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    pt = unpad(cipher.decrypt(ct), AES.block_size).decode("UTF-8")
    return pt


if __name__ == "__main__":
    if sys.argv[1] == "make":
        create_enc()
    if sys.argv[1] == "test":
        key = "AAAAAAAAAAAAAAAAAAAAAMaNZbAYiscqMHY+VbGTKEFZd5J6DUKUg08s1amr8scHdEvZjzPelnYu2YAh9gowng=="

        actual = decrypt_encrypted_key(key)
        print(actual)
        actual = int(actual.split("-")[0], base=16)

        try_dec(actual-1, actual+2)
