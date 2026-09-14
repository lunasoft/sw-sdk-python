import setuptools

with open('README.md', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name='sw-sdk-python',
    version='0.0.14.1',
    description="SDK para Timbrado en SmarterWeb",
    url="https://github.com/lunasoft/sw-sdk-python",
    packages=setuptools.find_packages(exclude=["Test"]),
    license="MIT",
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=["requests"],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
