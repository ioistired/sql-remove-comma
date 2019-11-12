#!/usr/bin/env python3

import setuptools

setuptools.setup(
	name='sql-remove-comma',
	use_scm_version=True,
	author='Io Mintz',
	author_email='io@mintz.cc',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	license='BSD-2-Clause-Patent',
	py_modules=['sql_remove_comma'],
	setup_requires=['setuptools_scm'],
	install_requires=['sqlparse>=0.3.0,<0.4.0'],
)
