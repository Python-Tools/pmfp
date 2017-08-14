from codecs import open
from setuptools import setup, find_packages
from os import path

REQUIREMETS_DEV_FILE = 'requirements_dev.txt'
REQUIREMETS_TEST_FILE = 'requirements_test.txt'
REQUIREMETS_FILE = 'requirements.txt'
PROJECTNAME = 'pmfp'
VERSION = '0.3.0'
DESCRIPTION = 'a simple package manager for python like npm.'
URL = 'https://github.com/Python-Tools/pmfp'
AUTHOR = 'hsz'
AUTHOR_EMAIL = 'hsz1273327@gmail.com'
LICENSE = 'MIT'
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Documentation :: Sphinx',
]
KEYWORDS = ['tools','package manager']
PACKAGES = find_packages(exclude=['contrib', 'docs', 'test'])
ZIP_SAFE = False

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()
REQUIREMETS_DIR = path.join(HERE,"requirements")

with open(path.join(REQUIREMETS_DIR, REQUIREMETS_FILE), encoding='utf-8') as f:
    REQUIREMETS = f.readlines()

with open(path.join(REQUIREMETS_DIR, REQUIREMETS_DEV_FILE), encoding='utf-8') as f:
    REQUIREMETS_DEV = f.readlines()

with open(path.join(REQUIREMETS_DIR, REQUIREMETS_TEST_FILE), encoding='utf-8') as f:
    REQUIREMETS_TEST = f.readlines()
setup(
    name=PROJECTNAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=PACKAGES,
    install_requires=REQUIREMETS,
    extras_require={
        'dev': REQUIREMETS_DEV,
        'test': REQUIREMETS_TEST
    },
    entry_points={'console_scripts': ['ppm = libpmfp.main:main']},
    zip_safe=ZIP_SAFE,
    include_package_data=True, # use MANIFEST.in during install
    data_files=[('requirements', ['requirements/requirements.txt', 'requirements/requirements_dev.txt', 'requirements/requirements_test.txt'])]
)
