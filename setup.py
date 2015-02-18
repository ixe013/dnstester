#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
    dnspython,
]

test_requirements = [
    # TODO: put package test requirements here
    udns
]

setup(
    name='dnstester',
    version='0.1.0',
    description="Simple tool to do bulk verifications of DNS entries taken from a CSV file.",
    long_description=readme + '\n\n' + history,
    author="Guillaume Seguin",
    author_email='guillaume@paralint.com',
    url='https://github.com/ixe013/dnstester',
    packages=[
        'dnstester',
    ],
    package_dir={'dnstester':
                 'dnstester'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='dnstester',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
