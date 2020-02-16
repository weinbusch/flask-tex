import os
import tempfile
from subprocess import run, PIPE, CalledProcessError


class TexError(Exception):
    pass


def run_tex(source, command="pdflatex"):
    with tempfile.TemporaryDirectory() as tempdir:
        return compile_source(source, command, tempdir)


def compile_source(source, command, directory):
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
