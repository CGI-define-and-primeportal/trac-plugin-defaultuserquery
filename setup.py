#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013 CGI Sweden

from setuptools import setup

setup(
    name='DefaultUserQueryPlugin',
    version=0.1,
    description='Allows users to select a default query to be used when ' +
                'visiting the ticket page',
    author="Anders Oscarsen",
    author_email="anders.oscarsen@cgi.com",
    license='BSD',
    url='http://define.primeportal.com/',
    packages=['defaultuserquery'],
    entry_points={
        'trac.plugins': [
            'defaultuserquery.defaultuserquery = ' +
            'defaultuserquery.defaultuserquery',
        ]
    },
)
