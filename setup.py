from setuptools import setup, find_packages

setup(
    name='iam_builder',
    version='0.0.2',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A lil python package to generate iam policies',
    long_description=open('README.md').read(),
    url='https://github.com/moj-analytical-services/iam_builder',
    author='Karik Isichei',
    author_email='karik.isichei@digital.justice.gov.uk',
    entry_points={
        'console_scripts': ['iam_builder=iam_builder.command_line:main'],
    }
)