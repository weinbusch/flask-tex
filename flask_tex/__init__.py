import os
import tempfile
from subprocess import run, PIPE, CalledProcessError

from flask import render_template, make_response


def render_to_pdf(template_name, filename="flask.pdf", **kwargs):
    source = render_template(template_name, **kwargs)
    pdf = compile_source(source)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f'filename="{filename}"'
    return response


class TexError(Exception):
    pass


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
