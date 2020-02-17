import os
import tempfile
from subprocess import run, PIPE, CalledProcessError

from markupsafe import Markup
from flask import render_template, make_response


class TexError(Exception):
    pass


class TeX:
    """TeX Flask extension"""

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        app.jinja_env.filters.update(
            linebreaks=do_linebreaks, latex_escape=do_latex_escape,
        )


def do_linebreaks(value):
    return value.replace("\n", "\\\\\n")


def do_latex_escape(value):
    return Markup(
        value.replace("&", "\\&")
        .replace("$", "\\$")
        .replace("%", "\\%")
        .replace("#", "\\#")
        .replace("_", "\\_")
        .replace("{", "\\{")
        .replace("}", "\\}")
    )


def render_to_pdf(template_name, filename="flask.pdf", **kwargs):
    source = render_template(template_name, **kwargs)
    pdf = compile_source(source)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f'filename="{filename}"'
    return response


def compile_source(source, command="pdflatex"):
    with tempfile.TemporaryDirectory() as tempdir:
        return run_tex(source, command, tempdir)


def run_tex(source, command, directory):
    filename = "texput.tex"
    with open(os.path.join(directory, filename), "x", encoding="utf-8") as f:
        f.write(source)
    args = f'cd "{directory}" && {command} -interaction=batchmode {filename}'
    try:
        run(args, shell=True, stdout=PIPE, stderr=PIPE, check=True)
    except CalledProcessError:
        try:
            with open(os.path.join(directory, "texput.log"), "r") as f:
                log = f.read()
                raise TexError(log)
        except FileNotFoundError:
            pass
        raise
    with open(os.path.join(directory, "texput.pdf"), "rb") as f:
        pdf = f.read()
    return pdf
