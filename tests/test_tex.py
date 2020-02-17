import pytest
from subprocess import CalledProcessError

from flask import Flask

from flask_tex import compile_source, TexError, render_to_pdf


class TestRunTex:

    source = (
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "This is a test\n"
        "\\end{document}\n"
    )

    def test_run_tex(self):
        pdf = compile_source(self.source)
        assert pdf is not None

    def test_run_tex_custom_latex_command(self):
        command = "lualatex"
        pdf = compile_source(self.source, command=command)
        assert pdf is not None

    def test_run_latexmk(self):
        command = "latexmk -pdf"
        pdf = compile_source(self.source, command=command)
        assert pdf is not None

    def test_run_unkown_command(self):
        command = "unknown"
        with pytest.raises(CalledProcessError):
            compile_source(self.source, command=command)

    def test_run_incorrect_source(self):
        source = "\\documentclass{article}\n" "\\begin{document}\n" "This is a test.\n"
        with pytest.raises(TexError):
            compile_source(source)


class TestApp:
    def test_render_template_to_pdf(self):
        app = Flask(__name__)

        with app.test_request_context():
            rv = render_to_pdf("test.tex", foo="bar")

        assert rv.status_code == 200
