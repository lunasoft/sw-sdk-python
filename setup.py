import setuptools
setuptools.setup(
    name='sw-sdk-python',
    version='0.0.5.1',
    description="SDK para Timbrado en SmarterWeb",
    url="https://github.com/lunasoft/sw-sdk-python",
    packages=setuptools.find_packages(),
    long_description_content_type="text/markdown",
    long_description=open('README.md',encoding='utf-8').read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
