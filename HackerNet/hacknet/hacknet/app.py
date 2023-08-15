import os
import uuid
import datetime
import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .models import AuthorizedToken, Victim, Credits

from flask import (
    Flask,
    render_template_string,
    session,
    render_template,
    request,
    abort,
    jsonify,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)


@app.route("/")
def index():
    if session.get("authorized", None):
        return render_template_string(
            """\
            <body>YOURE NOT SUPPOSED TO BE HERE!!!</body>\
            """
        )
    return render_template("hackernet.html", credits=Credits.select())


@app.route("/api/get_signing_key", methods=["POST"])
def get_signing_key():
    if not (token := request.headers.get("X-Hacker-Token", None)):
        abort(404)

    if not (tok := AuthorizedToken.get_or_none(token=token)):
        print("bad token")
        abort(400)

    if not request.form:
        print("no form")
        abort(400)

    if not request.form.get("file", None):
        print("no file")
        abort(400)

    key = b"uah{k3y_3ncryp7_1ng_k3y}"
    key = base64.b64encode(key)
    key = key.ljust(32, b"=")
    cipher = AES.new(key, AES.MODE_CFB, iv=bytes(AES.block_size))

    uuid_ = uuid.uuid1(clock_seq=69)
    timestamp = datetime.datetime(1582, 10, 15) + datetime.timedelta(
        microseconds=uuid_.time // 10
    )
    pt = bytes(str(uuid_), encoding="UTF-8")

    ct = base64.b64encode(cipher.iv + cipher.encrypt(pad(pt, AES.block_size))).decode(
        "UTF-8"
    )

    victim = Victim.create(date=timestamp, file_=request.form.get("file"), signing_key=ct)
    Credits.create(pwner=tok, pwn=victim)

    return jsonify(dict(token=ct)), 200


def get_victim_key():
    return os.urandom(32)


if __name__ == "__main__":
    app.run()
