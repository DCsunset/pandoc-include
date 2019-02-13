from setuptools import setup

VERSION = '0.1.0'

setup(
    name='pandoc-include',
    version=VERSION,
    description='Panflute filter to allow file includes',
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

