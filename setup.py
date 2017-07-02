from __future__ import with_statement

import setuptools

requires = [
    "flake8 > 3.0.0",
]

setuptools.setup(
    name="flake8-network-timeout",
    license="MIT",
    version="0.2.0",
    description="our extension to flake8",
    author="Messense Lv",
    author_email="messense@icloud.com",
    url="https://gitlab.com/messense/flake8-network-timeout",
    py_modules=[
        "flake8_network_timeout",
    ],
    install_requires=requires,
    entry_points={
        'flake8.extension': [
            'T60 = flake8_network_timeout:NetworkTimeoutLinter',
        ],
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
