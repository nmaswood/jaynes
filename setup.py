from typing import List

from setuptools import find_packages, setup

REQUIRED_PACKAGES: List[str] = [
    'pymc3', 'python-dateutil', 'beautifulsoup4', 'scikit-learn'
]
DEV_PACKAGES: List[str] = [
    'mypy', 'flake8', 'pytest', 'python-language-server[all]'
]
GOOGLE_AUTH_PACKAGES: List[str] = [
    'google-api-python-client',
    'google-auth-httplib2',
    'google-auth-oauthlib',
]

version = '0.0.1'

setup(
    name='jaynes',
    version=version,
    install_requires=REQUIRED_PACKAGES + GOOGLE_AUTH_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description=('Probability utils'),
    extras_require={'dev': DEV_PACKAGES},
)

# conda install -c conda-forge jupyter_contrib_nbextensions


