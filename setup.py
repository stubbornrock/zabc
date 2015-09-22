#!/usr/bin/env python
#-*- coding:utf-8 -*-
from setuptools import setup, find_packages
setup(
    name = "zabbix_ceilometer_plugin",
    version = "0.1",
    packages = find_packages(),
    package_data = {'':['*.py']},
    data_files = [('/etc/zabc/',['conf/zabc.conf','conf/vm_meters.conf','conf/logging.cfg'])],
    entry_points = {
        'console_scripts': [
            'zabc = zabc.proxy:main',
        ],
    }
)

