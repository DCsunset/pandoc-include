from setuptools import setup

setup(
    name='pandoc-include',
    version='0.1.0',
    description='Panflute filter to allow file includes',
    author='DCsunset',
    license='MIT',
    url='https://github.com/DCsunset/pandoc-include',
    
    install_requires=['panflute>=1'],
    entry_points={
        'console_scripts': [
            'pandoc-include = pandoc-include:main'
        ]
    },
)

