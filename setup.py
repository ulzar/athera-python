from distutils.core import setup

setup(
    name='AtheraPython',
    version='0.1.0',
    author='Simon',
    packages=['athera', 'auth'],
    url='https://storage.googleapis.com/athera-api/1.0.0/athera-api.html',
    license='LICENSE',
    description='Python wrapper around the Athera APIs',
    long_description=open('README.md').read(),
    install_requires=[
        "requests",
    ],
)