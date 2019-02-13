from setuptools import setup
from os import path

version = '0.1.0'

# Long description
with open(path.join(path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setup(
    name='pandoc-include',
    version=version,
    description='Panflute filter to allow file includes',
    long_description=long_description,
    author='DCsunset',
    author_email='DCsunset@protonmail.com',
    license='MIT',
    url='https://github.com/DCsunset/pandoc-include',
    
    install_requires=['panflute>=1'],
    entry_points={
        'console_scripts': [
            'pandoc-include = pandoc_include:main'
        ]
    },
)

