import os
from setuptools import setup


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


setup(
    name='upgrade-requirements',
    version='1.7.0',
    description='Upgrade all your outdated requirements in a single command.',
    long_description=read('README.md'),
    author='Joe Esposito',
    author_email='joe@joeyespo.com',
    url='http://github.com/joeyespo/upgrade-requirements.py',
    license='MIT',
    platforms='any',
    py_modules=['upgrade_requirements'],
    entry_points={
        'console_scripts': [
            'upgrade-requirements = upgrade_requirements:main',
            'upreq = upgrade_requirements:main',
        ],
    },
)
