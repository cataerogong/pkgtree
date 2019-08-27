import sys
from setuptools import setup, find_packages

import pkgtree

setup(
    name="pkgtree",
    version=pkgtree.__version__,
    # packages=find_packages(),
    py_modules=['pkgtree'], # only one python file
    # scripts=['pkgtree.py'], # install to python/Scripts

    # package_data={
    #     # If any package contains *.txt or *.rst files, include them:
    #     '': ['*.txt', '*.rst'],
    #     # And include any *.msg files found in the 'hello' package, too:
    #     'hello': ['*.msg'],
    # },

    install_requires=['setuptools'],
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',

    # metadata to display on PyPI
    author="CataerogGong",
    author_email="cataerogong@gmail.com",
    description="pkgtree",
    keywords="package tree pip uninstall helper",
    url="",   # project home page, if any
    project_urls={
        "Bug Tracker": "",
        "Documentation": "",
        "Source Code": "",
    },
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ],

    # could also include long_description, download_url, etc.
    entry_points={
        'console_scripts': [
            'pkgtree = pkgtree:main',
        ]
    }
)