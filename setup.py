#!/usr/bin/env python
"""
sentry-auth-adfs-oauth2
==================

:copyright: (c) 2016 Functional Software, Inc
"""
from setuptools import setup, find_packages


install_requires = [
    'sentry>=7.0.0',
]

tests_require = [
    'flake8>=2.0,<2.1',
]

setup(
    name='sentry-auth-adfs-oauth2',
    version='0.0.1.dev0',
    author='CCP Games',
    author_email='teamtechco@ccpgames.com',
    url='https://www.ccpgames.com',
    description='ADFS OAuth2 authentication provider for Sentry',
    long_description=__doc__,
    license='MIT',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'tests': tests_require},
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'auth_adfs_oauth2 = sentry_auth_adfs_oauth2',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
