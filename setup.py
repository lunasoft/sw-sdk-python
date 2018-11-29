import setuptools
# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='latin_1') as f:
    long_description = f.read()
setuptools.setup(
    name='sw-sdk-python',
    version='0.0.0.3dev2',
    author="Juan Gamez",
    author_email="juan.gamez@sw.com.mx",
    description="SDK para Timbrado en SmarterWeb",
    url="https://github.com/lunasoft/sw-sdk-python",
    packages=setuptools.find_packages(),
    long_description_content_type="text/markdown",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
