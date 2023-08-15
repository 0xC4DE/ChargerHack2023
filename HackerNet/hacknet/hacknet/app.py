import os
import base64

from Crypto.Cipher import AES

from .models import AuthorizedToken, Victim

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
    if not session.get("authorized", None):
        return render_template_string(
            """\
            <body>YOURE NOT SUPPOSED TO BE HERE!!!</body>\
            """
        )
    return render_template("templates/hackernet.html")


@app.route("/api/get_signing_key", methods=["POST"])
def get_signing_key():
    if not (token := request.headers.get("X-Hacker-Token", None)):
        abort(404)

    if not AuthorizedToken.get_or_none(token=token):
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
    print(key)
    cipher = AES.new(key, AES.MODE_CFB, iv=bytes(16))

    pt = b"1234567890123456"

    ct = base64.b64encode(cipher.encrypt(pt)).decode("UTF-8")

    Victim.create(file_=request.form.get("file"), signing_key=ct)

    return jsonify(dict(token=ct)), 200


def get_victim_key():
    return os.urandom(32)


if __name__ == "__main__":
    app.run()

