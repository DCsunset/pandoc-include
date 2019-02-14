from setuptools import setup
from os import path
import pypandoc

version = '0.3.0'

repo_base_dir = path.abspath(path.dirname(__file__))

# Long description
readme = path.join(repo_base_dir, 'README.md')
long_description = pypandoc.convert(readme, 'rst')

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
    # Add to lib so that it can be included
    py_modules=['pandoc_include'],
    entry_points={
        'console_scripts': [
            'pandoc-include = pandoc_include:main'
        ]
    },
)

