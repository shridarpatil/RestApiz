#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
    'pymysql', 'Flask',
]

setup_requirements = [
    'pytest-runner',
    'pymysql',
    'Flask',
    # TODO(shridarpatil): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    'pymysql',
    'Flask',
    # TODO: put package test requirements here
]

setup(
    name='RestApiz',
    version='0.1.0',
    description="Create rest api's dynamically within no time.",
    long_description=readme + '\n\n' + history,
    author="Shridhar Patil",
    author_email='shridharpatil2792@gmail.com',
    url='https://github.com/shridarpatil/RestApiz',
    download_url='https://github.com/shridarpatil/Flask-RestApi/archive/0.1.0.tar.gz',
    packages=find_packages(include=['RestApiz']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='RestApiz',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
