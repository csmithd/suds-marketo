# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='suds_marketo',
    version='0.0.1',
    author=u'Arthur Rio',
    author_email='arthur@punchtab.com',
    packages=find_packages(),
    url='https://github.com/PunchTab/suds-marketo',
    license='BSD licence, see LICENCE',
    description='Marketo SOAP Api made simple',
    long_description=open('README.md').read(),
    install_requires=[
        "Django >= 1.3",
        "suds == 0.4"
    ],
    zip_safe=False,
)

