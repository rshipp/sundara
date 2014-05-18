import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

requirements = open(os.path.join(os.path.dirname(__file__),
            'requirements.txt')).read()
requires = requirements.strip().split('\n')

setup(
    name='sundara',
    version='0.1',
    packages=['sundara'],
    scripts=['sundara/sundara'],
    include_package_data=True,
    install_requires=requires,
    license='BSD New',
    description='Yet another static website generator.',
    long_description=README,
    url='https://github.com/george2/sundara',
    author='george2',
    author_email='rpubaddr0@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
    ],
)
