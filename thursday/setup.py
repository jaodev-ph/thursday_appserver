import os
from setuptools import setup, find_packages

def parse_requirements(filename):
    here = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(here, filename)
    with open(filepath) as f:
        return [line for line in f.read().splitlines() if line and not line.startswith('#')]

setup(
    name='thursday',
    version='0.0',
    description='thursday unified library',
    url='',
    author='AnonymousComp',
    author_email='admin@whalebytes.co',
    packages=find_packages(include=['thursday', 'thursday.*']),  # ← explicit
    package_data={
        'thursday': ['*.yaml', '*.yml', '*.json'],  # ← include yaml/json files
    },
    install_requires=parse_requirements("requirements.txt"),
    zip_safe=False,
    include_package_data=True,
)