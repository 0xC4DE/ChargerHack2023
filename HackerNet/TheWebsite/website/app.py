import os
from flask import Flask, render_template_string, session, render_template

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


@app.route("/api/get_auth_key")
def auth_key():
    ...
