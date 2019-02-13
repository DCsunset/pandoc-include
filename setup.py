from setuptools import setup

setup(
    name='pandoc-include',
    version='0.1.0',
    description='Panflute filter to allow file includes',
    
    install_requires=['panflute>=1'],
    entry_points={
        'console_scripts': [
            'pandoc-include = pandoc-include:main'
        ]
    },

    author='DCsunset',
    license='MIT',
)

