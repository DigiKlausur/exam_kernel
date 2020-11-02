from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='exam_kernel',
    version='0.1',
    packages=['exam_kernel'],
    description='Restricted python kernel for Jupyter',
    long_description=readme,
    author='Tim Metzler',
    author_email='tim.metzler@h-brs.de',
    url='https://github.com/DigiKlausur/exam_kernel',
    install_requires=[
        'jupyter_client', 'IPython', 'ipykernel'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: MIT',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=['pytest-cov']
)
