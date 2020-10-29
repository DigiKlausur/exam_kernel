import os
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()


setup(
    name='exam_kernel',
    version='0.1',
    description='Restricted python kernel for Jupyter',
    long_description=readme,
    author='Tim Metzler',
    author_email='tim.metzler@h-brs.de',
    url='https://github.com/DigiKlausur/exam_kernel',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: MIT',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    package_data={
        '': ['*.json']
    },
    install_requires=[
        'jupyter_client', 'IPython', 'ipykernel'
    ],
    
)