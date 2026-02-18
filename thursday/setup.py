import os
from setuptools import setup, find_packages

def parse_requirements(filename):
    here = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(here, filename)
    with open(filepath) as f:
        return f.read().splitlines()

setup(
    name='thursday',
    version='0.0',
    description='thursday unified library',
    url='',
    author='AnonymousComp',
    author_email='admin@whalebytes.co',
    python_requires='~=3.6.5',
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    zip_safe=False,
    include_package_data=True,
    test_suite="tests"
)

