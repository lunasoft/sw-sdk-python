from distutils.core import setup

setup(
    name='sw-sdk-python',
    version='0.0.0.3dev',
    packages=['AcceptReject','Auth','Balance','Cancelation','Issue','Pdf','Pendings','Relations','Stamp','StatusCfdi','Validate'],
    long_description=open('README.md').read(),
)
