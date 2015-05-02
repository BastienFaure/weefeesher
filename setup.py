from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
#with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()

setup(
    name='weefeesher',
    version='1.0.0',
    description='PoC tool for assisted Wifi-based phishing',
    #long_description=long_description,
    url='https://www.github.com/BastienFaure/weefeesher',
    author='b0z',
    author_email='bastien@faure.io',
    license='MIT',
    classifiers=[
        'Development Status :: Alpha',
        'Intended Audience :: All',
        'Topic :: Security Audit :: Wifi Pentesting tools',
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='wifi pentest poc aircrack',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[],
    package_data={
       'weefeesher': [
           'templates/sites/*',
           'conf/dnsmasq.conf'
           ]
    },
    entry_points={
        'console_scripts': [
            'weefeesher=weefeesher:main',
        ],
    },
)

