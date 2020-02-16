import pytest
from subprocess import CalledProcessError

from flask_tex import run_tex, TexError


class TestRunTex:

    source = (
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "This is a test\n"
        "\\end{document}\n"
    )

    def test_run_tex(self):
        pdf = run_tex(self.source)
        assert pdf is not None

    def test_run_tex_custom_latex_command(self):
        command = "lualatex"
        pdf = run_tex(self.source, command=command)
        assert pdf is not None

    def test_run_latexmk(self):
        command = "latexmk -pdf"
        pdf = run_tex(self.source, command=command)
        assert pdf is not None

    def test_run_unkown_command(self):
        command = "unknown"
        with pytest.raises(CalledProcessError):
            run_tex(self.source, command=command)

    def test_run_incorrect_source(self):
        source = "\\documentclass{article}\n" "\\begin{document}\n" "This is a test.\n"
        with pytest.raises(TexError):
            run_tex(source)
