from flask import Flask

from flask_tex import render_to_pdf, TeX


app = Flask(__name__)
TeX(app)


@app.route("/")
def index():
    return render_to_pdf("index.tex", foo="Hello World")
