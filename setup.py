#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 CGI

from setuptools import setup

setup(
    name='DefaultUserQueryPlugin',
    version=0.1,
    description='Allows users to select a default query to be used when ' +
                'visiting the ticket page',
    author="Anders Oscarsen",
    author_email="anders.oscarsen@cgi.com",
    maintainer="CGI CoreTeam",
    maintainer_email="coreteam.service.desk.se@cgi.com",
    contact="CGI CoreTeam",
    contact_email="coreteam.service.desk.se@cgi.com",
    classifiers=['License :: OSI Approved :: BSD License'],
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
