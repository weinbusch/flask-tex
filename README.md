# flask-tex

`flask-tex` offers helper functions for using LaTeX from within a Flask
app. `flask-tex` requires a local LaTeX installation and uses `pdflatex`
by default.

## Usage

Import `flask_tex.render_to_pdf` and use it like `flask.render_template`
in your view function.

```python
from flask import Flask
from flask_tex import render_to_pdf


app = Flask(__name__)


@app.route("/")
def return_pdf_response():
    return render_to_pdf("tex_template.tex", foo="Hello World!")
```

Your template might look like this and should be located in place where `flask`
can find it.

```tex
\documentclass{article}

\title{Using \LaTeX{} with Flask}

\begin{document}

\maketitle

{{ foo }}

\end{document}
```

For lower level access to LaTeX, use `flask.compile_source`:

```python
from flask_tex import compile_source

pdf = compile_source(source, command="pdflatex")
```

where `source` is a string containing a `tex` document and command is a string defining
the LaTeX command to use for compiling the source. The string should contain any optional
flags you would like to pass to the LaTeX executable. The default `command` is `pdflatex`, but
you can supply others, e.g. `latexmk -pdf`. `pdf` is a bytes object containing the pdf file.

`compile_source` runs LaTeX inside a temporary directory. Use `flask_tex.run_tex`
to circumvent this and run LaTeX in a directory of your choice:

```python
from flask_tex import run_tex

pdf = run_tex(source, command="pdflatex", directory="/foo/bar/")
```

## Jinja integration

For deeper jinja integration, use `flask_tex` as an extension:

```python
from flask import Flask
from flask_tex import TeX

app = Flask(__app__)
TeX(app)
```

This adds some LaTeX specific filters to the jinja environment.

- LaTeX escape: `{{ foo | latex_escape }}` where `foo = "&$%#_{}"` renders as `"\\&\\$\\%\\#\\_\\{\\}"`.
    Danger: Do not use this in a html template, because the escaped string is marked as safe
    with `Markup`, so code that might be dangerous in html does not get escaped.

- LaTeX linebreaks: The `linebreaks` filter converts `\n` into `\\\\\n`.
