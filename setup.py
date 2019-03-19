from typing import List

from setuptools import find_packages, setup

REQUIRED_PACKAGES: List[str] = ['pymc3']
DEV_PACKAGES: List[str] = ['mypy', 'flake8', 'pytest']

version = '0.0.1'

setup(
    name='jaynes',
    version=version,
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description=('Probability utils'),
    extras_require={'dev': DEV_PACKAGES},
)
