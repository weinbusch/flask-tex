import pytest
from subprocess import CalledProcessError

from flask import Flask, render_template_string, render_template

from flask_tex import compile_source, TexError, render_to_pdf, TeX


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

    def test_no_autoescaping_in_tex_templates(self):
        app = Flask(__name__)

        with app.test_request_context():
            rv = render_template("test.tex", foo="This \\& sign will not be escaped")

        assert "This \\& sign will not be escaped" in rv

    def test_newline_filter(self):
        app = Flask(__name__)
        TeX(app)

        template_string = "{{ foo | linebreaks }}"

        foo = "bar\nbaz"

        with app.test_request_context():
            rv = render_template_string(template_string, foo=foo)

        assert rv == "bar\\\\\nbaz"

    def test_latex_escape(self):
        app = Flask(__name__)
        TeX(app)

        template_string = "{{ foo | latex_escape }}"
        foo = "&$%#_{}"

        with app.test_request_context():
            rv = render_template_string(template_string, foo=foo)

        assert (
            rv == "\\&\\$\\%\\#\\_\\{\\}"
        )  # This works because latex_escape marks the escaped string as safe with `Markup`
