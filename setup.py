from setuptools import setup

setup(
    name='readme',
    version='0.1',
    py_modules=['readme'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        readme=readme.readme:cli
    ''',
)