from setuptools import setup

setup(
    name='enlightenme',
    version='0.1',
    py_modules=['enlightenme'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        enlightenme=enlightenme.enlightenme:cli
    ''',
)