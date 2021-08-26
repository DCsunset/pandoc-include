from setuptools import setup
from os import path

version = '1.0.0'

repo_base_dir = path.abspath(path.dirname(__file__))

# Long description
readme = path.join(repo_base_dir, 'README.md')
with open(readme) as f:
    long_description = f.read()

setup(
    name='pandoc-include',
    version=version,
    description='Pandoc filter to allow file and header includes',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='DCsunset',
    author_email='DCsunset@protonmail.com',
    license='MIT',
    url='https://github.com/DCsunset/pandoc-include',

    install_requires=['panflute>=2.0.5', 'natsort>=7'],
    # Add to lib so that it can be included
    packages=["pandoc_include"],
    entry_points={
        'console_scripts': [
            'pandoc-include = pandoc_include.main:main'
        ]
    },

    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License'
    ]
)
