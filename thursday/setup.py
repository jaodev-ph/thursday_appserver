import os
from setuptools import setup, find_packages
setup(
    name='thursday',
    version='0.0',
    description='thursday unified library',
    url='',
    author='AnonymousComp',
    author_email='admin@whalebytes.co',
    # packages=find_packages(include=['thursday', 'thursday.*']),  # ← explicit
    # install_requires=parse_requirements("requirements.txt"),
    package_data={
        'thursday': ['*.yaml'],  # ← this needs to be here
    },
    zip_safe=False,
    include_package_data=True,
)