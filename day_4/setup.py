from setuptools import setup

with open("./README.md") as fp:
    long_description = fp.read()

with open("./requirements.txt") as fp:
    dependencies = [line.strip() for line in fp.readlines()]

setup(
    name="ACME Sales Forecast",
    version="0.1",
    description="Machine Learning for sales forecasting at ACME Inc.",
    long_description=long_description,
    author="YOUR NAME",
    author_email="YOUR EMAIL",
    packages=["src"],
    install_requires=dependencies,
)