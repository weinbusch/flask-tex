from flask import Flask

from flask_tex import render_to_pdf


app = Flask(__name__)


@app.route("/")
def index():
    return render_to_pdf("test.tex", foo="Hello World")
