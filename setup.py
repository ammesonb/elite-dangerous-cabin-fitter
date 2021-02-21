"""
Handles setup for the module
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elite-dangerous-cabin-fitter",
    version="1.0.0",
    author="Brett Ammeson",
    author_email="ammesonb@gmail.com",
    description=("Uses a naive algorithm to provide a best-fit for ED passenger missions"),
    long_description=long_description,
    url="https://github.com/ammesonb/elite-dangerous-cabin-fitter",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)
