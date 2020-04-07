from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="flask-tex",
    description="LaTeX integration for flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weinbusch/flask-tex",
    author="Martin Bierbaum",
    license="MIT",
    keywords="python flask latex",
    packages=find_packages(exclude=["tests"]),
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=["flask>=1.1.1"],
    python_requires=">=3.6.8",
    package_data={"": ["*.tex"]},
)
