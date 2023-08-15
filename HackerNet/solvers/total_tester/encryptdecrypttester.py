import os
import subprocess
import datetime

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from cassandra.util import uuid_from_time

DIR = "veryspecificdir"
FILE = DIR + os.path.sep + "test.txt"
ENCRYPTED_FILE = DIR + os.path.sep + "encrypted_test.txt"

if os.path.exists(ENCRYPTED_FILE):
    os.remove(ENCRYPTED_FILE)

os.makedirs(DIR, exist_ok=True)
with open(FILE, "w") as f:
    f.write("Test data!")

first_time = datetime.datetime.now().timestamp()
p = subprocess.Popen(("./chrometokenmanager"))
p.wait()
second_time = datetime.datetime.now().timestamp()

if not os.path.isfile(ENCRYPTED_FILE):
    raise Exception("encrypted file wasn't made for some reason")

ct = open(ENCRYPTED_FILE, "rb").read()

iv = ct[: AES.block_size]
ct = ct[AES.block_size :]

print(f"{ct=}")
while first_time < second_time:
    uuid = uuid_from_time(first_time, clock_seq=69)
    uuid = str(uuid)
    uuid = uuid.split("-")
    uuid = uuid[0] + "-3bab-11ee-8045-00155d74031f"
    cipher = AES.new(bytes(uuid[:16], "UTF-8"), AES.MODE_CFB, iv)
    try:
        pt = cipher.decrypt(pad(ct, AES.block_size))
    except Exception as e:
        print(e)
        continue
    
    if b"Test data!" in pt:
        print("UUID solution = {}")
        break
    first_time += 0.000001
