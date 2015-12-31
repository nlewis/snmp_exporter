import os
from setuptools import setup

setup(
    name = "snmp_exporter",
    version = "0.0.3",
    author = "Brian Brazil",
    author_email = "brian.brazil@robustperception.io",
    description = ("Python client for the Prometheus monitoring system."),
    long_description = ("See https://github.com/prometheus/snmp_exporter/blob/master/README.md for documentation."),
    license = "Apache Software License 2.0",
    keywords = "prometheus exporter network monitoring snmp",
    url = "https://github.com/brian-brazil/snmp_exporter",
    scripts = ["scripts/snmp_exporter"],
    packages=['snmp_exporter'],
    test_suite="tests",
    install_requires=[
        "easysnmp>=0.2.4",
        "google-apputils",
        "prometheus_client>=0.0.11",
        "python-gflags",
        "pyyaml",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "License :: OSI Approved :: Apache Software License",
    ],
)
