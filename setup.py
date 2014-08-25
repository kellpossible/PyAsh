from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import os
import sys
import codecs
import pyash

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
	encoding = kwargs.get('encoding', 'utf-8')
	sep = kwargs.get('sep', '\n')
	buf = []
	for filename in filenames:
		with io.open(filename, encoding=encoding) as f:
			buf.append(f.read())
	return sep.join(buf)

long_description = read('README.md')


setup(
	name='pyash',
	version=pyash.__version__,
	url='http://github.com/kellpossible/pyash',
	license='',
	author='Luke Frisken',
	author_email='l.frisken@gmail.com',
	test_suite='tests',
	install_requires=[],
	description='Port of the Ashley Framework to Python',
	long_description=long_description,
	packages=['pyash'],
	include_package_date=True,
	platforms='any',
	classifiers=[
		'Programming Language :: Python',
		'Operating System :: OS Independent',
		'Topic :: Software Development :: Libraries :: Python Modules'
	]
)